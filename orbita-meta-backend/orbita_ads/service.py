import base64
import threading
import time
from . import assets, validation as v
from .meta import MetaClient, MockMeta, MetaError
from .planner import plan
from .store import Store


class Pausing(Exception):
    pass


def resolve(value, results):
    if isinstance(value, dict) and set(value) == {"$ref"}:
        key, field = value["$ref"].split(".")
        return results[key][field]
    if isinstance(value, dict):
        return {k: resolve(x, results) for k, x in value.items()}
    if isinstance(value, list):
        return [resolve(x, results) for x in value]
    return value


class Service:
    def __init__(self, config, client=None):
        self.c = config
        self.store = Store(config.db_path)
        self.meta = client or (MockMeta() if config.mode == "mock" else MetaClient(config))
        self.execution_lock = threading.Lock()
        self.stop = threading.Event()

    def live_guard(self):
        if self.c.mode == "live" and not self.c.live_enabled:
            raise v.Problem("Habilitá ENABLE_LIVE_PUBLISH=true después de configurar Meta", 409, "LIVE_DISABLED")

    def connection(self, p=None):
        p = p or self.store.profile()
        if self.c.mode == "mock":
            return {"mode": "mock", "connected": False, "simulated": True,
                    "account": {"id": p["account_id"], "currency": p["currency"]}}
        account = self.meta.call("GET", p["account_id"], {"fields": "id,name,currency,account_status,timezone_name"})
        v.require(account.get("currency") == p["currency"], "Moneda del perfil distinta a la cuenta Meta")
        v.require(account.get("account_status") == 1, "La cuenta Meta no está activa")
        page = self.meta.call("GET", p["page_id"], {"fields": "id,name"})
        if p.get("pixel_id"):
            self.meta.call("GET", p["pixel_id"], {"fields": "id,name"})
        if p.get("instagram_user_id"):
            self.meta.call("GET", p["instagram_user_id"], {"fields": "id,username"})
        return {"mode": "live", "connected": True, "account": account, "page": page,
                "note": "Lectura verificada; los permisos de creación y la compatibilidad final los valida Meta al publicar"}

    def draft(self, body):
        return self.store.draft(plan(body, self.store.profile()))

    def from_link(self, body):
        v.obj(body, {"source_url", "source_type", "name", "structure", "thumbnail_url", "shared", "daily_budget_minor", "bid_cap_minor", "target_status"}, ("source_url", "source_type"))
        v.https(body["source_url"])
        v.require(body["source_type"] in ("image", "video", "manifest"), "source_type: image, video o manifest")
        if body["source_type"] == "manifest":
            v.require(set(body) == {"source_url", "source_type"}, "El manifiesto debe contener todos los parámetros; no se mezclan overrides externos")
            raw = assets.fetch(body["source_url"], self.c.asset_hosts, 256 * 1024, json_file=True)
        else:
            v.require("name" in body, "Falta name")
            media = {"kind": body["source_type"], "url": body["source_url"]}
            if "thumbnail_url" in body:
                media["thumbnail_url"] = body["thumbnail_url"]
            raw = {k: val for k, val in body.items() if k in v.REQUEST_FIELDS}
            raw.setdefault("structure", "ABO_1_1_1")
            raw["media"] = [media]
        return self.draft(raw)

    def publish(self, ident, body, idem):
        self.live_guard()
        v.obj(body, {"plan_hash"}, ("plan_hash",))
        v.text(idem, "Idempotency-Key", 128)
        p = self.store.get_draft(ident)
        v.require(body["plan_hash"] == p["plan_hash"], "El hash no corresponde al borrador")
        return self.store.enqueue(ident, idem, self.c.mode)

    def results(self, ident):
        return {s["key"]: s["result"] for s in self.store.job(ident)["steps"] if s["state"] == "DONE"}

    def check_pause(self, ident):
        if self.stop.is_set() or self.store.job(ident)["pause_requested"]:
            raise Pausing()

    def execute_step(self, job, op, results):
        ident, key, kind = job["id"], op["key"], op["kind"]
        if key in results:
            return results[key]
        old = next((s for s in self.store.job(ident)["steps"] if s["key"] == key), None)
        if old and old["state"] in ("UNCERTAIN", "IN_FLIGHT"):
            raise MetaError("RECONCILIATION_REQUIRED", ambiguous=True)
        body, path = resolve(op["body"], results), resolve(op["path"], results)
        # Download before the IN_FLIGHT marker: failures here never create remote objects.
        try:
            if kind == "image":
                data = assets.fetch(body["url"], self.c.asset_hosts) if self.c.mode == "live" else body["url"].encode()
                body = {"bytes": base64.b64encode(data).decode()}
            if kind == "video" and self.c.mode == "live":
                assets.resolve_public(body["file_url"], self.c.asset_hosts)
            if "name" in body:
                body["name"] += f" [orbita:{ident[:12]}:{key}]"
        except v.Problem as e:
            self.store.step(ident, key, "FAILED", error=str(e))
            raise
        self.check_pause(ident)
        if kind == "existing":
            self.store.step(ident, key, "DONE", body)
            return body
        if kind == "video_ready":
            for _ in range(30):
                self.check_pause(ident)
                data = self.meta.call("GET", path, {"fields": "status"})
                status = data.get("status", {}).get("video_status")
                if status == "ready":
                    result = {"id": path, "ready": True}
                    self.store.step(ident, key, "DONE", result)
                    return result
                if status == "error":
                    raise v.Problem("Meta no pudo procesar el video", 422, "VIDEO_FAILED")
                self.stop.wait(2)
            raise v.Problem("Video aún procesándose; reintentar conserva video_id", 409, "VIDEO_PROCESSING")
        self.store.step(ident, key, "IN_FLIGHT")
        try:
            response = self.meta.call("POST", path, body)
            if kind == "image":
                result = {"hash": next(iter(response["images"].values()))["hash"]}
            else:
                result = {"id": str(response["id"])}
                v.ident(result["id"], "Meta id")
        except MetaError as e:
            self.store.step(ident, key, "UNCERTAIN" if e.ambiguous else "FAILED", error=str(e))
            raise
        except Exception:
            self.store.step(ident, key, "UNCERTAIN", error="Respuesta de creación incompleta; verificar objeto remoto")
            raise MetaError("INCOMPLETE_CREATE_RESPONSE", ambiguous=True)
        self.store.step(ident, key, "DONE", result)
        self.store.event(ident, "created", {"step": key, **result})
        return result

    def set_status(self, remote_id, status):
        response = self.meta.call("POST", remote_id, {"status": status})
        if response.get("success") is not True:
            raise MetaError("STATUS_NOT_CONFIRMED", ambiguous=True)

    def pause_parents(self, ident, p):
        errors = []
        results = self.results(ident)
        for op in p["operations"]:
            if op["kind"] == "campaign" and op["key"] in results:
                remote_id = results[op["key"]]["id"]
                try:
                    self.set_status(remote_id, "PAUSED")
                    self.store.event(ident, "paused", {"campaign_id": remote_id})
                except Exception:
                    errors.append(remote_id)
        return errors

    def run(self, ident):
        with self.execution_lock:
            job = self.store.job(ident)
            p = self.store.get_draft(job["draft_id"])
            if job["mode"] != self.c.mode:
                self.store.state(ident, "FAILED", "Modo diferente al original; no mezclar mock y live")
                return
            try:
                self.live_guard()
                self.check_pause(ident)
                self.connection(p["profile"])
                results = self.results(ident)
                for op in p["operations"]:
                    self.check_pause(ident)
                    results[op["key"]] = self.execute_step(job, op, results)
                activate = bool(job["activate_requested"]) or p["request"]["target_status"] == "ACTIVE"
                if activate:
                    # Parents last. All children exist before any campaign can spend.
                    # Status writes are naturally idempotent; replay all on retry.
                    for kind in ("ad", "adset", "campaign"):
                        for op in p["operations"]:
                            if op["kind"] == kind:
                                self.check_pause(ident)
                                self.set_status(results[op["key"]]["id"], "ACTIVE")
                                self.store.event(ident, "activation_requested", {"step": op["key"], "id": results[op["key"]]["id"]})
                self.store.state(ident, "SIMULATED" if self.c.mode == "mock" else
                                 ("ACTIVATION_REQUESTED" if activate else "CREATED_PAUSED"))
            except Pausing:
                failures = self.pause_parents(ident, p)
                self.store.state(ident, "PAUSE_INCOMPLETE" if failures else "STOPPED_PAUSED",
                                 "No se confirmó pausa: " + ",".join(failures) if failures else None)
                self.store.clear_pause(ident)
            except Exception as e:
                failures = self.pause_parents(ident, p)
                uncertain = any(s["state"] in ("IN_FLIGHT", "UNCERTAIN") for s in self.store.job(ident)["steps"])
                msg = str(e) if isinstance(e, v.Problem) else "Fallo interno; revisar registro técnico sin exponer secretos"
                if failures:
                    msg += "; pausa no confirmada para campañas: " + ",".join(failures)
                self.store.state(ident, "NEEDS_RECONCILIATION" if uncertain or failures else "FAILED", msg)
                self.store.event(ident, "failed", {"code": e.code if isinstance(e, v.Problem) else "INTERNAL_ERROR"})

    def worker(self):
        while not self.stop.is_set():
            pending = self.store.pending_pause()
            if pending:
                try:
                    self.pause(pending)
                except v.Problem as e:
                    self.store.state(pending, "PAUSE_INCOMPLETE", str(e))
                    self.store.clear_pause(pending)
                continue
            ident = self.store.claim()
            if ident:
                self.run(ident)
            else:
                self.stop.wait(0.5)

    def pause(self, ident):
        self.live_guard()
        job = self.store.job(ident)
        v.require(job["mode"] == self.c.mode, "El trabajo pertenece a otro modo")
        self.store.request_pause(ident)
        if not self.execution_lock.acquire(blocking=False):
            return {"job_id": ident, "pause_requested": True, "note": "El worker pausará al terminar la llamada en curso; consultar estado"}
        try:
            job = self.store.job(ident)
            p = self.store.get_draft(job["draft_id"])
            failures = self.pause_parents(ident, p)
            uncertain = any(s["state"] in ("UNCERTAIN", "IN_FLIGHT") for s in job["steps"])
            if uncertain:
                self.store.state(ident, "NEEDS_RECONCILIATION", "Pausados los padres conocidos; quedan creaciones inciertas")
            else:
                self.store.state(ident, "PAUSE_INCOMPLETE" if failures else "STOPPED_PAUSED",
                                 "No se confirmó pausa: " + ",".join(failures) if failures else None)
            self.store.clear_pause(ident)
            return self.store.job(ident)
        finally:
            self.execution_lock.release()

    def activate(self, ident, body):
        self.live_guard()
        v.obj(body, {"plan_hash"}, ("plan_hash",))
        job = self.store.job(ident)
        v.require(job["mode"] == self.c.mode, "El trabajo pertenece a otro modo")
        p = self.store.get_draft(job["draft_id"])
        v.require(body["plan_hash"] == p["plan_hash"], "Hash del plan incorrecto")
        v.require(len(self.results(ident)) == len(p["operations"]), "Solo se puede activar una estructura completamente creada")
        self.store.enqueue_activation(ident)
        self.store.event(ident, "activation_queued", {"plan_hash": p["plan_hash"]})
        return self.store.job(ident)

    def resolve_step(self, ident, body):
        self.live_guard()
        v.obj(body, {"step_key", "resolution", "remote_id", "evidence"}, ("step_key", "resolution", "evidence"))
        v.text(body["evidence"], "evidence (verificación realizada en Meta)", 500)
        v.require(body["resolution"] in ("ATTACH", "NOT_CREATED"), "resolution inválida")
        if not self.execution_lock.acquire(blocking=False):
            raise v.Problem("Worker ocupado; reintentá después", 409)
        try:
            job = self.store.job(ident)
            v.require(job["mode"] == self.c.mode and job["state"] == "NEEDS_RECONCILIATION", "Estado/modo incompatible")
            step = next((s for s in job["steps"] if s["key"] == body["step_key"]), None)
            v.require(step is not None and step["state"] == "UNCERTAIN", "Paso no incierto")
            p = self.store.get_draft(job["draft_id"])
            op = next(o for o in p["operations"] if o["key"] == body["step_key"])
            if body["resolution"] == "NOT_CREATED":
                v.require("remote_id" not in body, "NOT_CREATED no admite remote_id")
                self.store.step(ident, op["key"], "FAILED", error="Administrador verificó que no se creó")
            else:
                v.require(op["kind"] in ("campaign", "adset", "creative", "ad"), "Adjuntar imagen/video incierto requiere revisión manual; solo NOT_CREATED tras comprobar ausencia")
                remote = v.ident(body.get("remote_id"), "remote_id")
                fields = "id,name,account_id" + {"ad": ",adset_id", "adset": ",campaign_id"}.get(op["kind"], "")
                data = self.meta.call("GET", remote, {"fields": fields})
                marker = f"[orbita:{ident[:12]}:{op['key']}]"
                v.require(str(data.get("account_id")) == p["profile"]["account_id"][4:] and marker in data.get("name", ""), "Objeto remoto no coincide con cuenta/marcador de este trabajo")
                expected = resolve(op["body"], self.results(ident))
                for parent in ("campaign_id", "adset_id"):
                    if parent in expected:
                        v.require(str(data.get(parent)) == expected[parent], "El padre remoto no coincide")
                self.store.step(ident, op["key"], "DONE", {"id": remote})
            self.store.event(ident, "reconciled", {"step": op["key"], "resolution": body["resolution"], "evidence": body["evidence"]})
            return self.store.job(ident)
        finally:
            self.execution_lock.release()

    def remote(self, ident, action):
        job = self.store.job(ident)
        v.require(job["mode"] == self.c.mode, "Modo incompatible")
        p = self.store.get_draft(job["draft_id"])
        results = self.results(ident)
        out = []
        for op in p["operations"]:
            if op["key"] not in results:
                continue
            if action == "status" and op["kind"] in ("campaign", "adset", "ad"):
                data = self.meta.call("GET", results[op["key"]]["id"], {"fields": "id,name,status,effective_status"})
            elif action == "insights" and op["kind"] == "campaign":
                data = self.meta.call("GET", results[op["key"]]["id"] + "/insights", {"fields": "campaign_id,impressions,clicks,spend,actions", "date_preset": "today"})
            elif action == "previews" and op["kind"] == "ad":
                data = self.meta.call("GET", results[op["key"]]["id"] + "/previews", {"ad_format": "DESKTOP_FEED_STANDARD"})
            else:
                continue
            out.append({"step": op["key"], "data": data})
        return {"mode": self.c.mode, "job_id": ident, "results": out}

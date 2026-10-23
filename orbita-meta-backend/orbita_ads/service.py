import base64
import re
import threading
import time
from . import assets, validation as v
from .meta import MetaClient, MockMeta, MetaError
from .planner import plan
from .store import Store


class Pausing(Exception):
    pass


PREVIEW_FORMATS = ("DESKTOP_FEED_STANDARD", "MOBILE_FEED_STANDARD", "INSTAGRAM_STANDARD", "INSTAGRAM_STORY", "INSTAGRAM_REELS", "FACEBOOK_REELS_MOBILE")
# effective_status de Meta -> fase legible. ACTIVO no implica entrega: eso lo dicen las impresiones.
PHASES = {"ACTIVE": "ACTIVO", "PREAPPROVED": "ACTIVO", "PENDING_REVIEW": "EN_REVISION", "IN_PROCESS": "PROCESANDO",
          "DISAPPROVED": "RECHAZADO", "WITH_ISSUES": "CON_PROBLEMAS", "PENDING_BILLING_INFO": "FALTA_MEDIO_DE_PAGO",
          "PAUSED": "PAUSADO", "CAMPAIGN_PAUSED": "PAUSADO", "ADSET_PAUSED": "PAUSADO", "ARCHIVED": "ARCHIVADO", "DELETED": "ELIMINADO"}


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

    def draft(self, body, idem=None):
        if idem:
            v.text(idem, "Idempotency-Key", 128)
        return self.store.draft(plan(body, self.store.profile()), idem)

    def from_link(self, body, idem=None):
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
        return self.draft(raw, idem)

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
                assets.probe(body["file_url"], self.c.asset_hosts, "video")
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
        if kind == "video_thumbnail":
            data = self.meta.call("GET", f"{path}/thumbnails", {"fields": "uri,is_preferred"}).get("data") or []
            chosen = next((t for t in data if t.get("is_preferred")), data[0] if data else None)
            if not chosen or not str(chosen.get("uri", "")).startswith("https://"):
                raise v.Problem("Meta no generó una portada para el video; agregá una imagen de portada JPG/PNG", 422, "VIDEO_THUMBNAIL_MISSING")
            result = {"url": chosen["uri"]}
            self.store.step(ident, key, "DONE", result)
            return result
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
            if job["state"] != "RUNNING":
                # Una pausa pudo resolverse entre claim() y este lock; no ejecutar sobre un trabajo ya detenido.
                return
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
                activate = bool(job["activate_requested"]) or (p["request"]["target_status"] == "ACTIVE" and not job["hold_paused"])
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

    def remote(self, ident, action, ad_format="DESKTOP_FEED_STANDARD"):
        job = self.store.job(ident)
        v.require(job["mode"] == self.c.mode, "Modo incompatible")
        v.require(ad_format in PREVIEW_FORMATS, "Formato de preview no admitido")
        p = self.store.get_draft(job["draft_id"])
        results = self.results(ident)
        out = []
        for op in p["operations"]:
            if op["key"] not in results:
                continue
            remote_id = results[op["key"]]["id"] if "id" in results[op["key"]] else None
            if action == "status" and op["kind"] in ("campaign", "adset", "ad"):
                fields = "id,name,status,effective_status,issues_info" + (",ad_review_feedback" if op["kind"] == "ad" else "")
                data = self.meta.call("GET", remote_id, {"fields": fields})
                data["phase"] = PHASES.get(data.get("effective_status"), "DESCONOCIDO")
                if op["kind"] == "campaign":
                    life = self.meta.call("GET", remote_id + "/insights", {"fields": "impressions,spend", "date_preset": "maximum"}).get("data") or []
                    data["lifetime_impressions"] = sum(int(x.get("impressions") or 0) for x in life)
            elif action == "insights" and op["kind"] == "campaign":
                data = self.meta.call("GET", remote_id + "/insights", {"fields": "campaign_id,impressions,clicks,spend,actions", "date_preset": "today"})
            elif action == "previews" and op["kind"] == "ad":
                data = self.meta.call("GET", remote_id + "/previews", {"ad_format": ad_format})
            else:
                continue
            out.append({"step": op["key"], "kind": op["kind"], "data": data})
        response = {"mode": self.c.mode, "job_id": ident, "results": out}
        if action == "status":
            ads = [x["data"]["phase"] for x in out if x["kind"] == "ad"]
            response["summary"] = {"local_state": job["state"],
                                   "ads_by_phase": {ph: ads.count(ph) for ph in dict.fromkeys(ads)},
                                   "delivering": any(x["data"].get("lifetime_impressions", 0) > 0 for x in out if x["kind"] == "campaign"),
                                   "note": "ENTREGANDO solo si Meta informa impresiones; ACTIVO no implica entrega." if self.c.mode == "live"
                                           else "Simulación: ningún objeto existe en Meta."}
        return response

    def list_jobs(self, limit=50):
        return {"mode": self.c.mode, "jobs": self.store.list_jobs(limit)}

    def update_defaults(self, body):
        """Guarda defaults reutilizables (copy, destino, enlace visible, UTM) sin tocar cuenta ni presupuesto."""
        p = self.store.profile()
        p["defaults"] = {**p["defaults"], **v.copy_fields(body)}
        return self.store.save_profile(v.profile(p))

    def check_asset(self, body):
        v.obj(body, {"url", "kind"}, ("url", "kind"))
        v.require(body["kind"] in ("image", "video", "thumbnail"), "kind: image, video o thumbnail")
        return assets.probe(body["url"], self.c.asset_hosts, "image" if body["kind"] == "thumbnail" else body["kind"])

    def verify_setup(self):
        """Comprobación guiada. Distingue lectura verificada de escritura validada por Meta (validate_only, sin crear nada)."""
        p = self.store.profile()
        if self.c.mode == "mock":
            return {"mode": "mock", "simulated": True, "read_verified": False, "write_validated": False,
                    "note": "Modo simulación: no hay conexión real con Meta."}
        checks = {}
        def check(name, fn):
            try:
                checks[name] = {"ok": True, **fn()}
            except v.Problem as e:
                checks[name] = {"ok": False, "error": str(e)}
        check("token", lambda: {"identity": self.meta.call("GET", "me", {"fields": "id,name"})})
        def permissions():
            data = self.meta.call("GET", "me/permissions", {}).get("data") or []
            granted = sorted(x["permission"] for x in data if x.get("status") == "granted")
            return {"granted": granted, "ads_management": "ads_management" in granted}
        check("permissions", permissions)
        def account():
            a = self.meta.call("GET", p["account_id"], {"fields": "id,name,currency,account_status,timezone_name,disable_reason"})
            v.require(a.get("currency") == p["currency"], f"La cuenta usa {a.get('currency')}; el perfil dice {p['currency']}")
            v.require(a.get("account_status") == 1, f"La cuenta no está activa (account_status={a.get('account_status')})")
            return {"name": a.get("name"), "currency": a.get("currency"), "timezone": a.get("timezone_name")}
        check("account", account)
        check("page", lambda: {"name": self.meta.call("GET", p["page_id"], {"fields": "id,name"}).get("name")})
        if p.get("pixel_id"):
            check("pixel", lambda: {"name": self.meta.call("GET", p["pixel_id"], {"fields": "id,name"}).get("name")})
        if p.get("instagram_user_id"):
            def instagram():
                rows = self.meta.call("GET", p["account_id"] + "/connected_instagram_accounts", {"fields": "id,username", "limit": 100}).get("data") or []
                match = next((x for x in rows if str(x.get("id")) == p["instagram_user_id"]), None)
                v.require(match is not None, "La cuenta de Instagram no figura entre las conectadas a la cuenta publicitaria")
                return {"name": match.get("username")}
            check("instagram", instagram)
        def write():
            r = self.meta.call("POST", p["account_id"] + "/campaigns", {
                "name": "Orbita validación sin crear", "objective": "OUTCOME_SALES" if p["objective"] == "SALES" else "OUTCOME_TRAFFIC",
                "buying_type": "AUCTION", "status": "PAUSED", "special_ad_categories": [], "is_adset_budget_sharing_enabled": False,
                "execution_options": ["validate_only"]})
            v.require(r.get("success") is True, "Meta no confirmó la validación")
            return {"method": "validate_only"}
        check("write_campaign", write)
        read_ok = all(checks[k]["ok"] for k in checks if k not in ("permissions", "write_campaign"))
        return {"mode": "live", "read_verified": read_ok, "write_validated": checks["write_campaign"]["ok"],
                "live_publish_enabled": self.c.live_enabled, "checks": checks,
                "note": "write_validated prueba que Meta acepta crear campañas con este token sin crear nada. "
                        "Página, creatividades y anuncios se comprueban recién con el ensayo real pausado."}

    def discover(self, account_id=None):
        """Lista activos visibles para el token, con nombres legibles. Cada sección informa su propio error de permisos."""
        if account_id is not None:
            v.require(isinstance(account_id, str) and bool(re.fullmatch(r"act_[0-9]{1,40}", account_id)), "account_id debe ser act_123...")
        if self.c.mode == "mock":
            return {"mode": "mock", "simulated": True, "note": "Modo simulación: sin activos reales."}
        out = {"mode": "live"}
        def section(name, path, fields):
            try:
                out[name] = {"ok": True, "items": self.meta.call("GET", path, {"fields": fields, "limit": 100}).get("data") or []}
            except v.Problem as e:
                out[name] = {"ok": False, "error": str(e), "items": []}
        section("ad_accounts", "me/adaccounts", "id,name,currency,account_status,timezone_name")
        section("pages", "me/accounts", "id,name")
        if account_id:
            section("promote_pages", account_id + "/promote_pages", "id,name")
            section("pixels", account_id + "/adspixels", "id,name")
            section("instagram_accounts", account_id + "/connected_instagram_accounts", "id,username")
        return out

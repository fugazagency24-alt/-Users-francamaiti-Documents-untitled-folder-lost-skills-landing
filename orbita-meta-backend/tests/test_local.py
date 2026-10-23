"""App local: secretos, modo, subidas, sesión de la pantalla y asistente IA."""
import json
import os
import stat
import struct
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace
from orbita_ads import tools
from orbita_ads.assistant import Assistant
from orbita_ads.config import Config
from orbita_ads.meta import MetaClient, MetaError
from orbita_ads.server import make_server
from orbita_ads.service import Service
from orbita_ads.validation import Problem
from tests.test_backend import profile, request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "integration"))
import agent_tools  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", 1080, 1080) + b"\x00" * 64
MP4 = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 200
TOKEN = "EAAB" + "x" * 60


def block(**kw):
    return SimpleNamespace(**kw, to_dict=lambda: {k: v for k, v in kw.items()})


class FakeClaude:
    """Devuelve respuestas guionadas y registra lo que se le envió."""
    def __init__(self, script):
        self.script, self.sent = list(script), []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self.create))

    def create(self, **kw):
        self.sent.append(json.loads(json.dumps(kw["messages"], default=str)))
        assert kw["model"] == "claude-opus-5-5" and kw["fallbacks"] == "default"
        return self.script.pop(0)


class LocalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.config = Config(api_key="x" * 48, db_path=str(self.dir / "orbita.sqlite3"))
        self.s = Service(self.config)
        self.s.store.save_profile(profile())

    def tearDown(self):
        self.tmp.cleanup()

    def upload(self, data, name):
        tmp = self.dir / "in.part"
        tmp.write_bytes(data)
        return self.s.save_upload(tmp, name)

    def test_secrets_stay_on_server(self):
        with self.assertRaises(Problem):
            self.s.set_secret("meta_access_token", {"value": "corto"})
        out = self.s.set_secret("meta_access_token", {"value": TOKEN})
        self.assertNotIn(TOKEN, json.dumps(out))
        self.assertEqual(out["secrets"]["meta_access_token"], {"configured": True, "source": "servidor"})
        self.assertEqual(stat.S_IMODE(os.stat(self.dir / "secrets.json").st_mode), 0o600)
        self.assertEqual(self.s.c.meta_token, TOKEN)
        self.s.clear_secret("meta_access_token")
        self.assertFalse(self.s.settings()["secrets"]["meta_access_token"]["configured"])

    def test_mode_switch_and_live_guards(self):
        self.s.set_runtime({"mode": "live"})
        self.assertIsInstance(self.s.meta, MetaClient)
        with self.assertRaisesRegex(Problem, "deshabilitada"):
            self.s.live_guard()
        self.s.set_runtime({"live_enabled": True})
        with self.assertRaises(Problem) as e:
            self.s.live_guard()
        self.assertEqual(e.exception.code, "META_TOKEN_MISSING")
        self.s.set_secret("meta_access_token", {"value": TOKEN})
        self.s.live_guard()
        # Persistido: un reinicio conserva el modo elegido en pantalla.
        self.assertEqual(Service(self.config).c.mode, "live")
        with self.assertRaises(Problem):
            self.s.set_runtime({"mode": "prod"})

    def test_uploaded_files_publish_as_media(self):
        img = self.upload(PNG, "foto.png")
        vid = self.upload(MP4, "video.mp4")
        cover = self.upload(PNG, "portada.png")
        self.assertEqual((img["kind"], img["format"], img["width"]), ("image", "PNG", 1080))
        self.assertEqual((vid["kind"], vid["format"]), ("video", "MP4"))
        with self.assertRaises(Problem):
            self.upload(b"<html>no</html>" + b" " * 64, "pagina.mp4")
        r = request()
        r["media"] = [{"kind": "image", "upload_id": img["id"]}, {"kind": "video", "upload_id": vid["id"], "thumbnail_upload_id": cover["id"]}]
        d = self.s.draft(r)
        with self.assertRaises(Problem):
            self.s.draft({**r, "media": [{"kind": "video", "upload_id": img["id"]}]})
        j = self.s.publish(d["draft_id"], {"plan_hash": d["plan_hash"]}, "k")
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "SIMULATED")
        self.assertTrue(any(c[0] == "UPLOAD" for c in self.s.meta.calls))
        images = [c for c in self.s.meta.calls if c[1].endswith("/adimages")]
        self.assertEqual(len(images), 2)
        creative = [c[2] for c in self.s.meta.calls if c[1].endswith("/adcreatives")][1]
        self.assertIn("image_hash", creative["object_story_spec"]["video_data"])

    def test_uncertain_media_upload_is_retry_safe(self):
        d = self.s.draft(request())
        j = self.s.publish(d["draft_id"], {"plan_hash": d["plan_hash"]}, "k")
        original = self.s.meta.call
        def call(method, path, params=None):
            if path.endswith("/adimages"):
                raise MetaError("TIMEOUT", ambiguous=True)
            return original(method, path, params)
        self.s.meta.call = call
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "FAILED")
        self.s.meta.call = original
        self.s.store.retry(j["id"])
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "SIMULATED")

    def test_ui_session_and_csrf(self):
        server = make_server(self.s, "127.0.0.1", 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_port
        base = f"http://127.0.0.1:{port}"
        def call(path, method="GET", body=None, headers=None):
            req = urllib.request.Request(base + path, method=method, headers=headers or {},
                                         data=json.dumps(body).encode() if body is not None else None)
            try:
                with urllib.request.urlopen(req) as res:
                    return res.status, res.headers, res.read()
            except urllib.error.HTTPError as e:
                return e.code, e.headers, e.read()
        try:
            code, headers, html = call("/")
            self.assertEqual(code, 200)
            self.assertIn(b"Meta Ads", html)
            self.assertIn(b"Ejecuci", html)
            cookie = headers["Set-Cookie"].split(";")[0]
            self.assertIn("HttpOnly", headers["Set-Cookie"])
            self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
            self.assertEqual(call("/", headers={"Host": "evil.example"})[0], 403)
            self.assertEqual(call("/static/app.js")[0], 200)
            self.assertEqual(call("/v1/settings")[0], 401)
            self.assertEqual(call("/v1/settings", headers={"Cookie": cookie})[0], 200)
            json_h = {"Cookie": cookie, "Content-Type": "application/json"}
            self.assertEqual(call("/v1/secrets/meta_access_token", "PUT", {"value": TOKEN}, json_h)[0], 403)
            ok = {**json_h, "Origin": base}
            code, _, body = call("/v1/secrets/meta_access_token", "PUT", {"value": TOKEN}, ok)
            self.assertEqual(code, 200)
            self.assertNotIn(TOKEN.encode(), body)
            self.assertEqual(call("/v1/settings", headers={**json_h, "Origin": "https://evil.example"})[0], 403)
            self.assertEqual(call("/v1/settings", headers={"Cookie": cookie, "Host": "evil.example"})[0], 401)
            up = {"Cookie": cookie, "Origin": base, "X-File-Name": "foto%201.png", "Content-Type": "application/octet-stream"}
            req = urllib.request.Request(base + "/v1/uploads", method="POST", headers=up, data=PNG)
            with urllib.request.urlopen(req) as res:
                row = json.load(res)
            self.assertEqual((row["name"], row["kind"]), ("foto 1.png", "image"))
            self.assertEqual(call(f"/v1/uploads/{row['id']}/file", headers={"Cookie": cookie})[2], PNG)
            self.assertEqual(call("/v1/settings", headers={"Authorization": "Bearer " + self.config.api_key})[0], 200)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_assistant_runs_tools_and_keeps_history(self):
        d = self.s.draft(request(2))
        fake = FakeClaude([
            SimpleNamespace(stop_reason="tool_use", content=[
                block(type="text", text="Reviso y publico."),
                block(type="tool_use", id="t1", name="orbita_get_settings", input={}),
                block(type="tool_use", id="t2", name="orbita_publish_campaign", input={"draft_id": d["draft_id"], "plan_hash": d["plan_hash"]})]),
            SimpleNamespace(stop_reason="end_turn", content=[block(type="text", text="Listo: 2 campañas en cola, en pausa.")]),
            SimpleNamespace(stop_reason="end_turn", content=[block(type="text", text="Siguen en cola.")]),
        ])
        a = Assistant(self.s, client=fake, permissions=tools.ALL_PERMISSIONS)
        out = a.send(None, "Publicá el borrador")
        self.assertEqual(out["reply"], "Listo: 2 campañas en cola, en pausa.")
        self.assertEqual([x["tool"] for x in out["actions"]], ["orbita_get_settings", "orbita_publish_campaign"])
        self.assertTrue(all(x["ok"] for x in out["actions"]))
        self.assertEqual(len(self.s.list_jobs()["jobs"]), 1)
        results = fake.sent[1][-1]["content"]
        self.assertEqual([r["tool_use_id"] for r in results], ["t1", "t2"])
        a.send(out["conversation_id"], "¿Y ahora?")
        self.assertEqual(len(fake.sent[2]), 5)  # historial completo, sin reescribir
        visible = a.history(out["conversation_id"])["messages"]
        self.assertEqual([m["role"] for m in visible], ["user", "assistant", "assistant", "user", "assistant"])

    def test_assistant_permissions_enforced_by_backend(self):
        d = self.s.draft(request(1, active=True))
        args = {"draft_id": d["draft_id"], "plan_hash": d["plan_hash"]}
        self.assertIn("permiso", tools.execute(self.s, "orbita_publish_campaign", args, {"read"})["error"])
        self.assertIn("activate", tools.execute(self.s, "orbita_publish_campaign", args, {"publish"})["error"])
        self.assertTrue(tools.execute(self.s, "orbita_resolve", {}, tools.ALL_PERMISSIONS)["is_error"])
        self.assertTrue(tools.execute(self.s, "orbita_campaign_status", {"job_id": "x"}, tools.ALL_PERMISSIONS)["is_error"])
        self.assertEqual(tools.PERMISSIONS, agent_tools.PERMISSIONS)
        self.assertEqual({t["name"] for t in tools.TOOLS}, set(tools.PERMISSIONS))

    def test_assistant_without_key_explains(self):
        with self.assertRaises(Problem) as e:
            Assistant(self.s).send(None, "hola")
        self.assertIn(e.exception.code, ("AI_KEY_MISSING", "AI_UNAVAILABLE"))


if __name__ == "__main__":
    unittest.main()

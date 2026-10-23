"""Pruebas de las correcciones y agregados de la integración (v1.1)."""
import json
import struct
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch
from orbita_ads import assets
from orbita_ads.config import Config
from orbita_ads.meta import MockMeta, explain
from orbita_ads.planner import plan
from orbita_ads.service import Service
from orbita_ads.server import make_server
from orbita_ads.validation import Problem
from tests.test_backend import profile, request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "integration"))
import agent_tools  # noqa: E402


def creative(p):
    return next(o["body"] for o in p["operations"] if o["kind"] == "creative")


class FakeLiveMeta(MockMeta):
    """Respuestas con la forma real de Graph para el modo live, sin red."""
    def call(self, method, path, params=None):
        params = params or {}
        if method == "GET" and path == "act_123456":
            self.calls.append((method, path, params))
            return {"id": "act_123456", "name": "Cuenta prueba", "currency": "ARS", "account_status": 1, "timezone_name": "America/Argentina/Buenos_Aires"}
        if method == "GET" and path in ("234567", "345678"):
            self.calls.append((method, path, params))
            return {"id": path, "name": {"234567": "Página prueba", "345678": "Píxel prueba"}[path]}
        if method == "GET" and path == "me/adaccounts":
            self.calls.append((method, path, params))
            return {"data": [{"id": "act_123456", "name": "Cuenta prueba", "currency": "ARS", "account_status": 1}]}
        return super().call(method, path, params)


class V2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = Config(api_key="x" * 48, db_path=str(Path(self.tmp.name) / "test.db"))
        self.s = Service(self.config)
        self.s.store.save_profile(profile())

    def tearDown(self):
        self.tmp.cleanup()

    def job(self, body):
        d = self.s.draft(body)
        j = self.s.publish(d["draft_id"], {"plan_hash": d["plan_hash"]}, d["draft_id"])
        return d, j

    # Meta: desde v23 advantage_audience debe declararse al crear el conjunto.
    def test_advantage_audience_is_explicit(self):
        adset = next(o["body"] for o in plan(request(), profile())["operations"] if o["kind"] == "adset")
        self.assertEqual(adset["targeting"]["targeting_automation"], {"advantage_audience": 0})
        p = {**profile(), "advantage_audience": True, "age_max": 50}
        with self.assertRaises(Problem):
            plan(request(), p)
        p["age_max"] = 65
        adset = next(o["body"] for o in plan(request(), p)["operations"] if o["kind"] == "adset")
        self.assertEqual(adset["targeting"]["targeting_automation"], {"advantage_audience": 1})

    def test_utm_normalized_and_macros_literal(self):
        for pasted in ("?utm_source=fb&utm_content=%7B%7Bad.id%7D%7D", "https://x.example/?utm_source=fb&utm_content={{ad.id}}"):
            r = {**request(), "shared": {"utm_template": pasted}}
            self.assertEqual(creative(plan(r, profile()))["url_tags"], "utm_source=fb&utm_content={{ad.id}}")

    def test_duplicate_params_named(self):
        r = {**request(), "shared": {"destination_url": "https://tienda.example/p?utm_source=x", "utm_template": "utm_source=fb"}}
        with self.assertRaisesRegex(Problem, "utm_source"):
            plan(r, profile())

    def test_display_link_three_modes(self):
        auto = creative(plan(request(), profile()))["object_story_spec"]["link_data"]
        self.assertEqual(auto["caption"], "https://tienda.example")
        omit = creative(plan({**request(), "shared": {"display_url_mode": "OMIT_CUSTOM"}}, profile()))["object_story_spec"]["link_data"]
        self.assertNotIn("caption", omit)
        custom = {**request(), "shared": {"display_url_mode": "CUSTOM", "display_url": "www.tienda.example/oferta"}}
        self.assertEqual(creative(plan(custom, profile()))["object_story_spec"]["link_data"]["caption"], "https://www.tienda.example/oferta")
        r = request()
        r["media"] = [{"kind": "video", "video_id": "123", "thumbnail_url": "https://cdn.example/t.jpg"}]
        video = creative(plan(r, profile()))["object_story_spec"]["video_data"]
        self.assertEqual(video["call_to_action"]["value"]["link_caption"], "https://tienda.example")

    def test_video_without_cover_uses_meta_thumbnail(self):
        r = request()
        r["media"] = [{"kind": "video", "url": "https://cdn.example/v.mp4"}]
        d, j = self.job(r)
        self.assertEqual(d["summary"]["videos_with_meta_thumbnail"], 1)
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "SIMULATED")
        body = next(c[2] for c in self.s.meta.calls if c[1].endswith("/adcreatives"))
        self.assertEqual(body["object_story_spec"]["video_data"]["image_url"], "https://scontent.example/mock-thumb.jpg")
        self.assertTrue(any(c[1].endswith("/thumbnails") for c in self.s.meta.calls))

    def test_pause_between_claim_and_run_creates_nothing(self):
        d, j = self.job(request())
        self.s.store.claim()
        self.assertEqual(self.s.pause(j["id"])["state"], "STOPPED_PAUSED")
        self.s.run(j["id"])
        self.assertFalse([c for c in self.s.meta.calls if c[0] == "POST"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "STOPPED_PAUSED")

    def test_manual_pause_holds_auto_activation_until_activate(self):
        d, j = self.job(request(2, active=True))
        self.s.pause(j["id"])
        self.s.store.retry(j["id"])  # reanudar crea lo que falta, sin activar
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertFalse([c for c in self.s.meta.calls if c[2] == {"status": "ACTIVE"}])
        self.s.activate(j["id"], {"plan_hash": d["plan_hash"]})
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(len([c for c in self.s.meta.calls if c[2] == {"status": "ACTIVE"}]), 6)
        self.assertEqual(len([c for c in self.s.meta.calls if c[1].endswith("/campaigns")]), 2)

    def test_meta_error_detail_is_readable_and_sanitized(self):
        text = explain({"message": "Invalid parameter", "error_user_title": "Puja muy baja",
                        "error_user_msg": "Subí la puja. https://x.example/a?access_token=EAABBBCCCDDDEEEFFF1234 EAABBBCCCDDDEEEFFF1234"})
        self.assertIn("Puja muy baja", text)
        self.assertNotIn("EAABBBCCCDDDEEEFFF1234", text)
        self.assertNotIn("access_token", text)

    def test_links_that_are_not_files(self):
        for url in ("https://drive.google.com/drive/folders/abc", "https://drive.google.com/file/d/abc/view",
                    "https://www.dropbox.com/s/abc/v.mp4?dl=0", "https://we.tl/t-abc", "https://www.youtube.com/watch?v=x"):
            with self.subTest(url=url), self.assertRaises(Problem) as e:
                assets.resolve_public(url, ("*",))
            self.assertEqual(e.exception.code, "NOT_A_DIRECT_FILE")
        with patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))]):
            self.assertEqual(assets.resolve_public("https://cualquier-cdn.example/a.jpg", ("*",))[0], "cualquier-cdn.example")

    def test_probe_detects_html_and_video_formats(self):
        with patch.object(assets, "fetch", return_value=("text/html", b"<!doctype html><html>")):
            with self.assertRaises(Problem):
                assets.probe("https://cdn.example/v", ("*",), "video")
        with patch.object(assets, "fetch", return_value=("video/mp4", b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 40)):
            self.assertEqual(assets.probe("https://cdn.example/v.mp4", ("*",), "video")["format"], "MP4")
        png = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", 1080, 1350)
        with patch.object(assets, "fetch", return_value=png):
            self.assertEqual(assets.probe("https://cdn.example/a.png", ("*",), "image")[ "width"], 1080)

    def test_saved_utm_reused_and_explicit_override_wins(self):
        self.s.update_defaults({"utm_template": "?utm_source=meta&utm_campaign={{campaign.name}}"})
        self.assertEqual(self.s.store.profile()["defaults"]["utm_template"], "utm_source=meta&utm_campaign={{campaign.name}}")
        self.assertEqual(creative(self.s.draft(request()))["url_tags"], "utm_source=meta&utm_campaign={{campaign.name}}")
        override = {**request(), "shared": {"utm_template": "utm_source=otro"}}
        self.assertEqual(creative(self.s.draft(override))["url_tags"], "utm_source=otro")
        with self.assertRaises(Problem):
            self.s.update_defaults({"daily_budget_minor": 1})

    def test_remote_phases_and_listing(self):
        d, j = self.job(request(2))
        self.s.store.claim()
        self.s.run(j["id"])
        remote = self.s.remote(j["id"], "status")
        self.assertEqual(remote["summary"]["ads_by_phase"], {"PAUSADO": 2})
        self.assertFalse(remote["summary"]["delivering"])
        jobs = self.s.list_jobs()["jobs"]
        self.assertEqual([x["id"] for x in jobs], [j["id"]])
        self.assertEqual(jobs[0]["summary"]["campaigns"], 2)
        self.assertEqual(self.s.store.list_drafts()[0]["job_id"], j["id"])

    def test_live_setup_verification_creates_nothing(self):
        s = Service(Config(api_key="x" * 48, db_path=self.config.db_path, mode="live", meta_token="dummy"), FakeLiveMeta())
        out = s.verify_setup()
        self.assertTrue(out["read_verified"])
        self.assertTrue(out["write_validated"])
        self.assertEqual(out["checks"]["page"]["name"], "Página prueba")
        posts = [c for c in s.meta.calls if c[0] == "POST"]
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0][2]["execution_options"], ["validate_only"])
        self.assertFalse(s.meta.objects)
        found = s.discover("act_123456")
        self.assertEqual(found["ad_accounts"]["items"][0]["name"], "Cuenta prueba")
        self.assertTrue(found["pixels"]["ok"])

    def test_live_currency_mismatch_is_reported(self):
        p = profile()
        p["currency"] = "USD"
        self.s.store.save_profile(p)
        s = Service(Config(api_key="x" * 48, db_path=self.config.db_path, mode="live", meta_token="dummy"), FakeLiveMeta())
        out = s.verify_setup()
        self.assertFalse(out["read_verified"])
        self.assertIn("ARS", out["checks"]["account"]["error"])

    def test_agent_tools_enforce_backend_permissions(self):
        d = self.s.draft(request(1, active=True))
        sent = []
        def transport(method, path, body=None, idem=None):
            sent.append((method, path, idem))
            return {"draft_id": d["draft_id"], **self.s.store.get_draft(d["draft_id"])} if method == "GET" else {"ok": True}
        args = {"draft_id": d["draft_id"], "plan_hash": d["plan_hash"]}
        self.assertTrue(agent_tools.execute_tool("orbita_publish_campaign", args, permissions={"read"}, transport=transport)["is_error"])
        out = agent_tools.execute_tool("orbita_publish_campaign", args, permissions={"publish"}, transport=transport)
        self.assertIn("activate", out["error"])
        self.assertEqual(agent_tools.execute_tool("orbita_publish_campaign", args, permissions={"publish", "activate"}, transport=transport), {"ok": True})
        self.assertEqual(sent[-1], ("POST", f"/v1/drafts/{d['draft_id']}/publish", "orbita-" + d["draft_id"]))
        self.assertTrue(agent_tools.execute_tool("orbita_resolve", {}, permissions={"read", "publish"}, transport=transport)["is_error"])
        names = {t["name"] for t in agent_tools.tool_definitions({"read"})}
        self.assertNotIn("orbita_publish_campaign", names)
        self.assertIn("orbita_get_settings", names)

    def test_draft_idempotency_double_click(self):
        a = self.s.draft(request(), "click-1")
        b = self.s.draft(request(), "click-1")
        self.assertEqual(a["draft_id"], b["draft_id"])
        self.assertEqual(len(self.s.store.list_drafts()), 1)
        with self.assertRaises(Problem):
            self.s.draft(request(2), "click-1")
        self.assertNotEqual(self.s.draft(request())["draft_id"], a["draft_id"])

    def test_http_new_routes(self):
        server = make_server(self.s, "127.0.0.1", 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_port}"
        def call(path, body=None, method=None):
            req = urllib.request.Request(url + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                         headers={"Content-Type": "application/json", "Authorization": "Bearer " + self.config.api_key})
            with urllib.request.urlopen(req) as res:
                return json.load(res)
        try:
            self.assertEqual(call("/v1/profile/defaults", {"utm_template": "utm_source=a"}, "PUT")["defaults"]["utm_template"], "utm_source=a")
            self.assertTrue(call("/v1/setup/verify", {}, "POST")["simulated"])
            self.assertEqual(call("/v1/jobs?limit=5")["jobs"], [])
            self.assertEqual(call("/v1/drafts")["drafts"], [])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()

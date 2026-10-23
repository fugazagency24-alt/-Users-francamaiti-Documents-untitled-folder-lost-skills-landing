import copy
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch
from orbita_ads.assets import resolve_public
from orbita_ads.config import Config
from orbita_ads.meta import MockMeta, MetaError
from orbita_ads.planner import plan
from orbita_ads.service import Service
from orbita_ads.server import make_server
from orbita_ads.validation import Problem


def profile():
    return {"account_id": "act_123456", "page_id": "234567", "pixel_id": "345678", "currency": "ARS",
            "countries": ["AR"], "objective": "SALES", "daily_budget_minor": 100000,
            "max_batch_daily_budget_minor": 1000000, "bid_cap_minor": 50000,
            "defaults": {"primary_text": "Conocé nuestro producto.", "headline": "Conocé más", "cta": "LEARN_MORE",
                         "destination_url": "https://tienda.example/producto?origen=orbita",
                         "utm_template": "utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.id}}&utm_content={{ad.id}}"}}


def request(n=1, structure="ABO_1_1_1", active=False):
    return {"name": "Prueba", "structure": structure, "target_status": "ACTIVE" if active else "PAUSED",
            "media": [{"kind": "image", "url": f"https://cdn.example/ad-{i}.jpg"} for i in range(n)]}


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = Config(api_key="x" * 48, db_path=str(Path(self.tmp.name) / "test.db"))
        self.s = Service(self.config)
        self.s.store.save_profile(profile())

    def tearDown(self):
        self.tmp.cleanup()

    def job(self, body=None):
        d = self.s.draft(body or request())
        j = self.s.publish(d["draft_id"], {"plan_hash": d["plan_hash"]}, d["draft_id"])
        self.assertEqual(self.s.store.claim(), j["id"])
        return d, j

    def test_bid_cap_exact_structure_and_no_campaign_budget(self):
        p = plan(request(10, "BID_CAP_1_1_10"), profile())
        self.assertEqual([p["summary"][k] for k in ("campaigns", "adsets", "ads")], [1, 1, 10])
        adset = next(o["body"] for o in p["operations"] if o["kind"] == "adset")
        campaign = next(o["body"] for o in p["operations"] if o["kind"] == "campaign")
        self.assertEqual(adset["bid_amount"], 50000)
        self.assertEqual(adset["bid_strategy"], "LOWEST_COST_WITH_BID_CAP")
        self.assertNotIn("daily_budget", campaign)
        self.assertFalse(campaign["is_adset_budget_sharing_enabled"])
        with self.assertRaises(Problem):
            plan(request(9, "BID_CAP_1_1_10"), profile())

    def test_abo_budget_multiplies_per_creative(self):
        p = plan(request(3), profile())
        self.assertEqual(p["summary"]["campaigns"], 3)
        self.assertEqual(p["summary"]["total_daily_budget_minor"], 300000)
        with self.assertRaises(Problem):
            plan(request(11), profile())

    def test_copy_cta_display_utm_payload(self):
        r = request()
        r["shared"] = {"primary_text": "Texto común", "cta": "SHOP_NOW", "display_url_mode": "CUSTOM", "display_url": "https://tienda.example/oferta"}
        r["media"][0]["overrides"] = {"headline": "Título particular"}
        p = plan(r, profile())
        c = next(o["body"] for o in p["operations"] if o["kind"] == "creative")
        self.assertEqual(c["object_story_spec"]["link_data"]["caption"], "https://tienda.example/oferta")
        self.assertEqual(c["object_story_spec"]["link_data"]["call_to_action"]["type"], "SHOP_NOW")
        self.assertEqual(c["object_story_spec"]["link_data"]["name"], "Título particular")
        self.assertIn("{{ad.id}}", c["url_tags"])
        self.assertNotIn("utm_content", c["object_story_spec"]["link_data"]["link"])

    def test_display_and_utm_reject_bad_values(self):
        for shared in [{"display_url_mode": "HIDDEN"}, {"utm_template": "?a=b"},
                       {"utm_template": "a=b&a=c"}, {"utm_template": "a={{made.up}}"},
                       {"utm_template": "origen=duplicado"},
                       {"display_url_mode": "CUSTOM", "display_url": "https://otro.example"}]:
            with self.subTest(shared=shared), self.assertRaises(Problem):
                plan({**request(), "shared": shared}, profile())

    def test_plan_hash_freezes_defaults(self):
        d = self.s.draft(request())
        p = profile()
        p["defaults"]["primary_text"] = "Nuevo texto"
        self.s.store.save_profile(p)
        saved = self.s.store.get_draft(d["draft_id"])
        self.assertEqual(saved["plan_hash"], d["plan_hash"])
        self.assertNotEqual(saved["plan_hash"], plan(request(), p)["plan_hash"])
        with self.assertRaises(Problem):
            self.s.publish(d["draft_id"], {"plan_hash": "wrong"}, "key")

    def test_idempotency_dedup_and_conflict(self):
        d, j = self.job()
        again = self.s.publish(d["draft_id"], {"plan_hash": d["plan_hash"]}, "different-key")
        self.assertEqual(j["id"], again["id"])
        d2 = self.s.draft(request())
        with self.assertRaises(Problem):
            self.s.publish(d2["draft_id"], {"plan_hash": d2["plan_hash"]}, d["draft_id"])

    def test_full_mock_activates_parents_last_and_pause(self):
        d, j = self.job(request(2, active=True))
        self.s.run(j["id"])
        out = self.s.store.job(j["id"])
        self.assertEqual(out["state"], "SIMULATED")
        self.assertEqual(len([x for x in out["steps"] if x["key"].startswith("ad") and not x["key"].startswith("adset")]), 2)
        activations = [c for c in self.s.meta.calls if c[0] == "POST" and c[2] == {"status": "ACTIVE"}]
        campaigns = [s["result"]["id"] for s in out["steps"] if s["key"].startswith("campaign")]
        self.assertEqual([c[1] for c in activations[-2:]], campaigns)
        self.assertEqual(self.s.pause(j["id"])["state"], "STOPPED_PAUSED")

    def test_known_failure_retries_without_duplicate_creations(self):
        d, j = self.job()
        original = self.s.meta.call
        failed = [False]
        def call(method, path, params=None):
            if path.endswith("/ads") and not failed[0]:
                failed[0] = True
                raise MetaError(100)
            return original(method, path, params)
        self.s.meta.call = call
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "FAILED")
        self.s.store.retry(j["id"])
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "SIMULATED")
        self.assertEqual(len([c for c in self.s.meta.calls if c[1].endswith("/campaigns")]), 1)

    def test_ambiguous_creation_blocks_retry(self):
        d, j = self.job()
        original = self.s.meta.call
        def call(method, path, params=None):
            if path.endswith("/campaigns"):
                raise MetaError("TIMEOUT", ambiguous=True)
            return original(method, path, params)
        self.s.meta.call = call
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "NEEDS_RECONCILIATION")
        with self.assertRaises(Problem):
            self.s.store.retry(j["id"])
        self.s.resolve_step(j["id"], {"step_key": "campaign0", "resolution": "NOT_CREATED", "evidence": "Simulación de verificación de ausencia"})
        self.s.meta.call = original
        self.s.store.retry(j["id"])
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "SIMULATED")

    def test_restart_marks_uncertain(self):
        d, j = self.job()
        self.s.store.step(j["id"], "campaign0", "IN_FLIGHT")
        self.s.store.recover()
        self.assertEqual(self.s.store.job(j["id"])["steps"][0]["state"], "UNCERTAIN")
        self.assertEqual(self.s.store.job(j["id"])["state"], "NEEDS_RECONCILIATION")

    def test_activation_error_compensates_parents(self):
        d, j = self.job(request(2, active=True))
        original = self.s.meta.call
        def call(method, path, params=None):
            if params == {"status": "ACTIVE"}:
                raise MetaError(100)
            return original(method, path, params)
        self.s.meta.call = call
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "FAILED")
        self.assertEqual(len([c for c in self.s.meta.calls if c[2] == {"status": "PAUSED"}]), 2)

    def test_video_upload_and_processing(self):
        r = request()
        r["media"] = [{"kind": "video", "url": "https://cdn.example/video.mp4", "thumbnail_url": "https://cdn.example/thumb.jpg"}]
        d, j = self.job(r)
        self.s.run(j["id"])
        self.assertEqual(self.s.store.job(j["id"])["state"], "SIMULATED")
        self.assertTrue(any(c[1].endswith("/advideos") for c in self.s.meta.calls))
        c = next(c[2] for c in self.s.meta.calls if c[1].endswith("/adcreatives"))
        self.assertIn("image_hash", c["object_story_spec"]["video_data"])
        self.assertNotIn("link_data", c["object_story_spec"])

    def test_activate_existing_does_not_duplicate(self):
        d, j = self.job()
        self.s.run(j["id"])
        creations = len([c for c in self.s.meta.calls if c[1].endswith("/campaigns")])
        self.s.activate(j["id"], {"plan_hash": d["plan_hash"]})
        self.s.store.claim()
        self.s.run(j["id"])
        self.assertEqual(creations, len([c for c in self.s.meta.calls if c[1].endswith("/campaigns")]))
        self.assertEqual(len([c for c in self.s.meta.calls if c[2] == {"status": "ACTIVE"}]), 3)

    def test_custom_video_caption(self):
        r = request()
        r["media"] = [{"kind": "video", "video_id": "123456", "thumbnail_url": "https://cdn.example/thumb.jpg"}]
        r["shared"] = {"display_url_mode": "CUSTOM", "display_url": "https://tienda.example/oferta"}
        p = plan(r, profile())
        creative = next(o for o in p["operations"] if o["kind"] == "creative")
        self.assertEqual(creative["body"]["object_story_spec"]["video_data"]["call_to_action"]["value"]["link_caption"], "https://tienda.example/oferta")

    def test_sales_requires_pixel_and_unknown_fields_rejected(self):
        p = profile()
        del p["pixel_id"]
        with self.assertRaises(Problem):
            plan(request(), p)
        with self.assertRaises(Problem):
            plan({**request(), "special_ad_categories": ["CREDIT"]}, profile())

    def test_live_disabled_stops_publish(self):
        s = Service(Config(api_key="x" * 48, db_path=self.config.db_path, mode="live", meta_token="dummy"), MockMeta())
        d = s.draft(request())
        with self.assertRaises(Problem):
            s.publish(d["draft_id"], {"plan_hash": d["plan_hash"]}, "key")

    def test_asset_ssrf_and_allowlist(self):
        with self.assertRaises(Problem):
            resolve_public("https://evil.example/a.jpg", ("cdn.example",))
        with patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("127.0.0.1", 443))]):
            with self.assertRaises(Problem):
                resolve_public("https://cdn.example/a.jpg", ("cdn.example",))
        with patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("169.254.169.254", 443))]):
            with self.assertRaises(Problem):
                resolve_public("https://cdn.example/a.jpg", ("cdn.example",))

    def test_single_link_shortcut(self):
        d = self.s.from_link({"source_url": "https://cdn.example/ad.jpg", "source_type": "image", "name": "Link"})
        self.assertEqual(d["summary"]["ads"], 1)
        self.assertEqual(d["request"]["structure"], "ABO_1_1_1")

    def test_http_auth_profile_publish_status(self):
        server = make_server(self.s, "127.0.0.1", 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_port}"
        def call(path, body=None, auth=True, extra=None):
            headers = {"Content-Type": "application/json", **(extra or {})}
            if auth:
                headers["Authorization"] = "Bearer " + self.config.api_key
            req = urllib.request.Request(url + path, headers=headers, data=json.dumps(body).encode() if body is not None else None)
            with urllib.request.urlopen(req) as res:
                return json.load(res)
        try:
            with self.assertRaises(urllib.error.HTTPError) as e:
                call("/v1/profile", auth=False)
            self.assertEqual(e.exception.code, 401)
            with self.assertRaises(urllib.error.HTTPError) as e:
                call("/v1/profile", extra={"Origin": "https://evil.example"})
            self.assertEqual(e.exception.code, 403)
            d = call("/v1/drafts", request())
            j = call(f"/v1/drafts/{d['draft_id']}/publish", {"plan_hash": d["plan_hash"]}, extra={"Idempotency-Key": "http-test"})
            self.assertEqual(call(f"/v1/jobs/{j['id']}")["state"], "QUEUED")
            self.s.store.claim()
            self.s.run(j["id"])
            self.assertEqual(call(f"/v1/jobs/{j['id']}")["state"], "SIMULATED")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()

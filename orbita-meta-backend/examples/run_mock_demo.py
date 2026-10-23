"""Prueba local completa; no necesita Meta, red ni token. Ejecutar desde raíz."""
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orbita_ads.config import Config
from orbita_ads.service import Service


with tempfile.TemporaryDirectory() as tmp:
    service = Service(Config(api_key="demo-only-key-not-for-deployment-000000", db_path=str(Path(tmp) / "demo.db")))
    root = Path(__file__).parent
    service.store.save_profile(json.loads((root / "profile.json").read_text()))
    for name in ("bid-cap-1-1-10", "abo-1-1-1", "abo-video"):
        request = json.loads((root / f"{name}.json").read_text())
        draft = service.draft(request)
        job = service.publish(draft["draft_id"], {"plan_hash": draft["plan_hash"]}, name)
        service.store.claim()
        service.run(job["id"])
        result = service.store.job(job["id"])
        assert result["state"] == "SIMULATED", result
        print(json.dumps({"case": name, "state": result["state"], "summary": draft["summary"], "steps": len(result["steps"])}, ensure_ascii=False))

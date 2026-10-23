"""Adaptador ejecutable de tool calls para Claude/IA de Orbita. Solo backend."""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


def tool_definitions():
    return json.loads(Path(__file__).with_name("claude-tools.json").read_text())


def execute_tool(name, arguments, *, base_url=None, service_key=None):
    base = (base_url or os.environ.get("PUBLISHER_URL", "http://127.0.0.1:8787")).rstrip("/")
    key = service_key or os.environ["ORBITA_SERVICE_KEY"]
    body, idem, method = None, None, "GET"
    if name == "orbita_prepare_campaign":
        path, method, body = "/v1/drafts", "POST", arguments["request"]
    elif name == "orbita_prepare_from_link":
        path, method, body = "/v1/drafts/from-link", "POST", arguments["request"]
    elif name == "orbita_connection":
        path = "/v1/connection"
    elif name == "orbita_publish_campaign":
        ident = arguments["draft_id"]
        if not re.fullmatch(r"[a-f0-9]{32}", ident):
            raise ValueError("draft_id inválido")
        path, method, body, idem = f"/v1/drafts/{ident}/publish", "POST", {"plan_hash": arguments["plan_hash"]}, "orbita-" + ident
    elif name in ("orbita_campaign_status", "orbita_pause_campaign", "orbita_activate_campaign", "orbita_campaign_insights", "orbita_campaign_remote"):
        ident = arguments["job_id"]
        if not re.fullmatch(r"[a-f0-9]{32}", ident):
            raise ValueError("job_id inválido")
        suffix = {"orbita_campaign_status": "", "orbita_pause_campaign": "/pause", "orbita_activate_campaign": "/activate", "orbita_campaign_insights": "/insights", "orbita_campaign_remote": "/remote"}[name]
        path = f"/v1/jobs/{ident}{suffix}"
        if name == "orbita_pause_campaign":
            method, body = "POST", {}
        elif name == "orbita_activate_campaign":
            method, body = "POST", {"plan_hash": arguments["plan_hash"]}
    else:
        raise ValueError("Herramienta no autorizada")
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    if idem:
        headers["Idempotency-Key"] = idem
    req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(), headers=headers, method=method)
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        return {"is_error": True, "status": exc.code, "response": json.loads(exc.read())}


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "tools":
        print(json.dumps(tool_definitions(), ensure_ascii=False, indent=2))
    elif len(sys.argv) == 3:
        print(json.dumps(execute_tool(sys.argv[1], json.loads(sys.argv[2])), ensure_ascii=False, indent=2))
    else:
        raise SystemExit("Uso: python integration/agent_tools.py tools | TOOL_NAME '{JSON}'")

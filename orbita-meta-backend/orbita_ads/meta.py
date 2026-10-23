import hashlib
import hmac
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from .validation import Problem


class MetaError(Problem):
    def __init__(self, code=None, subcode=None, trace=None, ambiguous=False):
        # Do not persist raw provider messages, which may echo URLs or secrets.
        super().__init__(f"Meta rechazó o no confirmó la operación (code={code}, subcode={subcode}, trace={trace})",
                         502, "META_UNCERTAIN" if ambiguous else "META_ERROR")
        self.ambiguous = ambiguous


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class MetaClient:
    def __init__(self, config):
        self.c = config
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def call(self, method, path, params=None):
        if not re.fullmatch(r"(?:act_)?[0-9]+(?:/[a-z_]+)?", path):
            raise Problem("Ruta Graph interna inválida")
        params = dict(params or {})
        if self.c.meta_app_secret:
            params["appsecret_proof"] = hmac.new(self.c.meta_app_secret.encode(), self.c.meta_token.encode(), hashlib.sha256).hexdigest()
        form = urllib.parse.urlencode({k: json.dumps(v, separators=(",", ":")) if isinstance(v, (dict, list, bool)) else str(v) for k, v in params.items()})
        url = f"https://graph.facebook.com/{self.c.graph_version}/{path}"
        req = urllib.request.Request(url + ("?" + form if method == "GET" else ""),
                                     data=form.encode() if method == "POST" else None, method=method,
                                     headers={"Authorization": "Bearer " + self.c.meta_token,
                                              "Content-Type": "application/x-www-form-urlencoded"})
        # Automatic retries ONLY for reads. A POST timeout can have created an object.
        for attempt in range(3 if method == "GET" else 1):
            try:
                with self.opener.open(req, timeout=60) as response:
                    result = json.loads(response.read(8 * 1024 * 1024))
                if not isinstance(result, dict):
                    raise ValueError("Invalid Graph response")
                if "error" in result:
                    e = result["error"]
                    raise MetaError(e.get("code"), e.get("error_subcode"), e.get("fbtrace_id"), ambiguous=method == "POST")
                return result
            except urllib.error.HTTPError as exc:
                try:
                    e = json.loads(exc.read(65536)).get("error", {})
                except (ValueError, AttributeError):
                    e = {}
                if method == "GET" and (exc.code >= 500 or exc.code == 429) and attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                raise MetaError(e.get("code", exc.code), e.get("error_subcode"), e.get("fbtrace_id"),
                                ambiguous=method == "POST" and (exc.code >= 500 or exc.code in (408, 429)))
            except (OSError, ValueError):
                if method == "GET" and attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                raise MetaError("NETWORK_OR_BAD_RESPONSE", ambiguous=method == "POST")


class MockMeta:
    """Deterministic local simulator. Never sends network requests."""
    def __init__(self):
        self.calls = []
        self.objects = {}

    def call(self, method, path, params=None):
        params = params or {}
        self.calls.append((method, path, params))
        if method == "GET":
            if "video_status" in params.get("fields", "") or params.get("fields") == "status":
                return {"id": path, "status": {"video_status": "ready"}}
            if path.endswith("/insights"):
                return {"data": [], "mock": True}
            if path.endswith("/previews"):
                return {"data": [{"body": "<div>Simulación: no es una vista real de Meta</div>"}]}
            return {"id": path, **self.objects.get(path, {}), "mock": True}
        if path.endswith("/adimages"):
            return {"images": {"asset": {"hash": hashlib.sha256(params.get("bytes", "mock").encode()).hexdigest()[:32]}}}
        if re.fullmatch(r"[0-9]+", path):
            self.objects.setdefault(path, {}).update(params)
            return {"success": True}
        ident = str(int(hashlib.sha256((path + json.dumps(params, sort_keys=True)).encode()).hexdigest()[:14], 16))
        self.objects[ident] = {"id": ident, **params}
        return {"id": ident}

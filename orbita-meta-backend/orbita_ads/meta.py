import hashlib
import hmac
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from .validation import Problem


def explain(error):
    """Texto que Meta destina al usuario, sin tokens ni parámetros de URL que pueda repetir."""
    parts = [error.get(k) for k in ("error_user_title", "error_user_msg", "message") if isinstance(error.get(k), str)]
    text = " · ".join(dict.fromkeys(x.strip() for x in parts if x.strip()))
    text = re.sub(r"EAA[A-Za-z0-9]{10,}", "[token]", text)
    text = re.sub(r"(access_token|appsecret_proof|signature|sig)=[^&\s]+", r"\1=[oculto]", text, flags=re.I)
    text = re.sub(r"https?://\S+", lambda m: m.group(0).split("?")[0], text)
    return text[:400]


class MetaError(Problem):
    def __init__(self, code=None, subcode=None, trace=None, ambiguous=False, detail=""):
        # Solo el texto saneado que Meta destina al usuario; nunca la respuesta cruda.
        message = f"Meta rechazó o no confirmó la operación (code={code}, subcode={subcode}, trace={trace})"
        if detail:
            message += ": " + detail
        super().__init__(message, 502, "META_UNCERTAIN" if ambiguous else "META_ERROR")
        self.ambiguous, self.meta_code, self.meta_subcode = ambiguous, code, subcode


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class MetaClient:
    def __init__(self, config):
        self.c = config
        # Sin proxies salvo que el despliegue lo pida explícitamente (egress obligatorio por proxy).
        proxies = urllib.request.ProxyHandler() if config.meta_use_env_proxy else urllib.request.ProxyHandler({})
        self.opener = urllib.request.build_opener(proxies, NoRedirect())

    def call(self, method, path, params=None):
        if not re.fullmatch(r"(?:(?:act_)?[0-9]+|me)(?:/[a-z_]+)?", path):
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
                    raise MetaError(e.get("code"), e.get("error_subcode"), e.get("fbtrace_id"), ambiguous=method == "POST", detail=explain(e))
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
                                ambiguous=method == "POST" and (exc.code >= 500 or exc.code in (408, 429)), detail=explain(e))
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
            if path.endswith("/thumbnails"):
                return {"data": [{"uri": "https://scontent.example/mock-thumb.jpg", "is_preferred": True}]}
            if path.endswith("/insights"):
                return {"data": [], "mock": True}
            if path.endswith("/previews"):
                return {"data": [{"body": "<div>Simulación: no es una vista real de Meta</div>"}]}
            if path == "me":
                return {"id": "100000000000001", "name": "Usuario simulado", "mock": True}
            if path == "me/permissions":
                return {"data": [{"permission": "ads_management", "status": "granted"},
                                 {"permission": "ads_read", "status": "granted"}], "mock": True}
            if path in ("me/adaccounts", "me/accounts") or path.endswith(("/adspixels", "/connected_instagram_accounts", "/page_backed_instagram_accounts", "/promote_pages")):
                return {"data": [], "mock": True}
            stored = self.objects.get(path, {})
            status = stored.get("status", "PAUSED")
            return {"id": path, **stored, "effective_status": status, "mock": True}
        if "validate_only" in str(params.get("execution_options", "")):
            return {"success": True}
        if path.endswith("/adimages"):
            return {"images": {"asset": {"hash": hashlib.sha256(params.get("bytes", "mock").encode()).hexdigest()[:32]}}}
        if re.fullmatch(r"[0-9]+", path):
            self.objects.setdefault(path, {}).update(params)
            return {"success": True}
        ident = str(int(hashlib.sha256((path + json.dumps(params, sort_keys=True)).encode()).hexdigest()[:14], 16))
        self.objects[ident] = {"id": ident, **params}
        return {"id": ident}

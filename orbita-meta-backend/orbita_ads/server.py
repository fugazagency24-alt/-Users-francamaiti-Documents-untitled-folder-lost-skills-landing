import hmac
import json
import re
import secrets
import tempfile
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote
from . import validation as v
from . import __version__
from .planner import plan

WEB = Path(__file__).with_name("web")
STATIC = {"app.js": "text/javascript; charset=utf-8", "styles.css": "text/css; charset=utf-8", "icon.svg": "image/svg+xml"}
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; connect-src 'self'; "
       "frame-src https://www.facebook.com https://*.facebook.com; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")


def json_object(pairs):
    result = {}
    for k, val in pairs:
        if k in result:
            raise ValueError("Clave JSON duplicada")
        result[k] = val
    return result


def make_server(service, host=None, port=None):
    class Handler(BaseHTTPRequestHandler):
        server_version = "OrbitaPublisher/1.2"
        sys_version = ""

        def setup(self):
            super().setup()
            self.connection.settimeout(30)

        def log_message(self, fmt, *args):
            # No request URL/query/token/body in access logs.
            return

        def body(self):
            if self.headers.get("Transfer-Encoding"):
                raise v.Problem("No se admite Transfer-Encoding", 400)
            try:
                size = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise v.Problem("Content-Length inválido")
            if not 0 <= size <= 256 * 1024:
                raise v.Problem("JSON supera 256 KiB", 413)
            if size and self.headers.get_content_type() != "application/json":
                raise v.Problem("Usá Content-Type: application/json", 415)
            if not size:
                return {}
            try:
                def invalid_constant(value):
                    raise ValueError("Número JSON no finito")
                return json.loads(self.rfile.read(size), object_pairs_hook=json_object, parse_constant=invalid_constant)
            except (ValueError, UnicodeError):
                raise v.Problem("JSON inválido")

        def local_host(self):
            port = self.server.server_address[1]
            return self.headers.get("Host", "") in (f"127.0.0.1:{port}", f"localhost:{port}")

        def origins(self):
            port = self.server.server_address[1]
            return (f"http://127.0.0.1:{port}", f"http://localhost:{port}")

        def authorize(self):
            """Dos vías: clave de servicio (backend a backend, sin Origin) o sesión de la pantalla local (cookie + host + origin)."""
            origin = self.headers.get("Origin")
            if self.headers.get("Authorization"):
                if origin:
                    raise v.Problem("Servicio interno: llamar desde el backend de Orbita", 403)
                if not hmac.compare_digest(self.headers.get("Authorization", ""), "Bearer " + service.c.api_key):
                    raise v.Problem("No autorizado", 401)
                return
            cookie = SimpleCookie(self.headers.get("Cookie", "")).get("orbita_ui")
            if cookie and hmac.compare_digest(cookie.value, self.server.ui_token) and self.local_host():
                # Pedidos que cambian algo deben venir de esta misma pantalla (sin CSRF desde otros sitios).
                same_site = origin in self.origins() or (not origin and self.headers.get("Sec-Fetch-Site") == "same-origin")
                if (self.command != "GET" or origin) and not same_site:
                    raise v.Problem("Origen no permitido", 403)
                return
            raise v.Problem("No autorizado", 401)

        def upload(self):
            try:
                size = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise v.Problem("Content-Length inválido")
            v.require(0 < size <= 4096 * 1024 * 1024, "Archivo vacío o mayor a 4 GB")
            service.uploads_dir.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=service.uploads_dir, suffix=".part")
            with open(fd, "wb") as f:
                left = size
                while left:
                    block = self.rfile.read(min(left, 1024 * 1024))
                    if not block:
                        raise v.Problem("Subida incompleta")
                    f.write(block)
                    left -= len(block)
            return service.save_upload(tmp, unquote(self.headers.get("X-File-Name", "archivo")))

        def dispatch(self):
            path = urlsplit(self.path).path
            if self.command == "GET" and path == "/health":
                return 200, {"ok": True, "mode": service.c.mode, "version": __version__}
            self.authorize()
            method = self.command
            query = parse_qs(urlsplit(self.path).query)
            def arg(name, default=None):
                return query.get(name, [default])[0]
            def limit():
                raw = arg("limit", "50")
                v.require(raw.isdigit() and 1 <= int(raw) <= 200, "limit: 1 a 200")
                return int(raw)
            if method == "GET" and path == "/v1/settings":
                return 200, service.settings()
            if method == "PUT" and path == "/v1/settings/runtime":
                return 200, service.set_runtime(self.body())
            m = re.fullmatch(r"/v1/secrets/([a-z_]{1,40})", path)
            if m and method == "PUT":
                return 200, service.set_secret(m[1], self.body())
            if m and method == "DELETE":
                return 200, service.clear_secret(m[1])
            if method == "POST" and path == "/v1/uploads":
                return 201, self.upload()
            m = re.fullmatch(r"/v1/uploads/([a-f0-9]{32})(/file)?", path)
            if m and method == "GET":
                row = service.store.upload(m[1])
                if m[2]:
                    return 200, ("file", row)
                return 200, {k: row[k] for k in ("id", "name", "kind", "format", "size", "width", "height")}
            if method == "POST" and path == "/v1/assistant/messages":
                body = self.body()
                v.obj(body, {"conversation_id", "text"}, ("text",))
                return 200, service.assistant().send(body.get("conversation_id"), body["text"])
            m = re.fullmatch(r"/v1/assistant/conversations/([a-f0-9]{32})", path)
            if m and method == "GET":
                return 200, service.assistant().history(m[1])
            if path == "/v1/profile":
                if method == "GET":
                    return 200, service.store.profile()
                if method == "PUT":
                    return 200, service.store.save_profile(v.profile(self.body()))
            if method == "PUT" and path == "/v1/profile/defaults":
                return 200, service.update_defaults(self.body())
            if method == "GET" and path == "/v1/connection":
                return 200, service.connection()
            if method == "POST" and path == "/v1/setup/verify":
                v.obj(self.body(), set())
                return 200, service.verify_setup()
            if method == "GET" and path == "/v1/setup/assets":
                return 200, service.discover(arg("account_id"))
            if method == "POST" and path == "/v1/assets/check":
                return 200, service.check_asset(self.body())
            if method == "GET" and path == "/v1/jobs":
                return 200, service.list_jobs(limit())
            if method == "GET" and path == "/v1/drafts":
                return 200, {"drafts": service.store.list_drafts(limit())}
            if method == "POST" and path == "/v1/preview":
                return 200, plan(self.body(), service.store.profile())
            if method == "POST" and path == "/v1/drafts":
                return 201, service.draft(self.body(), self.headers.get("Idempotency-Key"))
            if method == "POST" and path == "/v1/drafts/from-link":
                return 201, service.from_link(self.body(), self.headers.get("Idempotency-Key"))
            m = re.fullmatch(r"/v1/drafts/([a-f0-9]{32})(/publish)?", path)
            if m:
                if method == "GET" and not m[2]:
                    return 200, {"draft_id": m[1], **service.store.get_draft(m[1])}
                if method == "POST" and m[2]:
                    return 202, service.publish(m[1], self.body(), self.headers.get("Idempotency-Key", ""))
            m = re.fullmatch(r"/v1/jobs/([a-f0-9]{32})(?:/(pause|activate|retry|resolve|remote|insights|previews))?", path)
            if m:
                ident, action = m.groups()
                if method == "GET" and not action:
                    return 200, service.store.job(ident)
                if method == "GET" and action in ("remote", "insights", "previews"):
                    return 200, service.remote(ident, "status" if action == "remote" else action, arg("format", "DESKTOP_FEED_STANDARD"))
                if method == "POST" and action == "pause":
                    v.obj(self.body(), set())
                    return 202, service.pause(ident)
                if method == "POST" and action == "activate":
                    return 202, service.activate(ident, self.body())
                if method == "POST" and action == "retry":
                    v.obj(self.body(), set())
                    service.live_guard()
                    v.require(service.store.job(ident)["mode"] == service.c.mode, "Modo incompatible")
                    return 202, service.store.retry(ident)
                if method == "POST" and action == "resolve":
                    return 200, service.resolve_step(ident, self.body())
            raise v.Problem("Ruta o método no encontrado", 404)

        def send_bytes(self, code, data, content_type, extra=()):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            for k, val in extra:
                self.send_header(k, val)
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(data)
            self.close_connection = True

        def page(self, path):
            """Pantalla local. Solo por 127.0.0.1/localhost: evita que otro sitio la sirva bajo su dominio (DNS rebinding)."""
            if not self.local_host():
                self.send_bytes(403, b"Abrir desde http://127.0.0.1", "text/plain; charset=utf-8")
                return True
            if path in ("/", "/index.html"):
                cookie = f"orbita_ui={self.server.ui_token}; HttpOnly; SameSite=Strict; Path=/"
                self.send_bytes(200, (WEB / "index.html").read_bytes(), "text/html; charset=utf-8",
                                (("Set-Cookie", cookie), ("Content-Security-Policy", CSP), ("Referrer-Policy", "no-referrer")))
                return True
            name = path[len("/static/"):] if path.startswith("/static/") else None
            if name in STATIC:
                self.send_bytes(200, (WEB / name).read_bytes(), STATIC[name])
                return True
            return False

        def respond(self):
            path = urlsplit(self.path).path
            if self.command == "GET" and (path in ("/", "/index.html") or path.startswith("/static/")) and self.page(path):
                return
            try:
                code, value = self.dispatch()
                if isinstance(value, tuple) and value[0] == "file":
                    # Por partes: un video puede pesar gigas y no debe cargarse entero en memoria.
                    row = value[1]
                    self.send_response(200)
                    self.send_header("Content-Type", {"PNG": "image/png", "JPG": "image/jpeg", "MP4": "video/mp4", "MOV": "video/quicktime"}[row["format"]])
                    self.send_header("Content-Length", str(Path(row["path"]).stat().st_size))
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.send_header("Connection", "close")
                    self.end_headers()
                    with open(row["path"], "rb") as f:
                        for block in iter(lambda: f.read(1024 * 1024), b""):
                            self.wfile.write(block)
                    self.close_connection = True
                    return
            except v.Problem as e:
                code, value = e.status, {"error": {"code": e.code, "message": str(e)}}
            except (TypeError, KeyError, AttributeError):
                code, value = 400, {"error": {"code": "INVALID_SHAPE", "message": "Tipos o estructura JSON no válidos"}}
            except Exception:
                code, value = 500, {"error": {"code": "INTERNAL_ERROR", "message": "Error interno del servicio"}}
            data = json.dumps(value, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(data)
            self.close_connection = True

        do_GET = respond
        do_POST = respond
        do_PUT = respond
        do_DELETE = respond
        do_OPTIONS = respond

    server = ThreadingHTTPServer((host or service.c.host, service.c.port if port is None else port), Handler)
    server.ui_token = secrets.token_urlsafe(32)
    return server

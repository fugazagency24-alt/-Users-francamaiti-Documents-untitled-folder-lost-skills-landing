import hmac
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from . import validation as v
from .planner import plan


def json_object(pairs):
    result = {}
    for k, val in pairs:
        if k in result:
            raise ValueError("Clave JSON duplicada")
        result[k] = val
    return result


def make_server(service, host=None, port=None):
    class Handler(BaseHTTPRequestHandler):
        server_version = "OrbitaPublisher/1.0"
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

        def dispatch(self):
            path = urlsplit(self.path).path
            if self.command == "GET" and path == "/health":
                return 200, {"ok": True, "mode": service.c.mode, "version": "1.0.0"}
            if self.headers.get("Origin"):
                raise v.Problem("Servicio interno: llamar desde el backend de Orbita", 403)
            if not hmac.compare_digest(self.headers.get("Authorization", ""), "Bearer " + service.c.api_key):
                raise v.Problem("No autorizado", 401)
            method = self.command
            if path == "/v1/profile":
                if method == "GET":
                    return 200, service.store.profile()
                if method == "PUT":
                    return 200, service.store.save_profile(v.profile(self.body()))
            if method == "GET" and path == "/v1/connection":
                return 200, service.connection()
            if method == "POST" and path == "/v1/preview":
                return 200, plan(self.body(), service.store.profile())
            if method == "POST" and path == "/v1/drafts":
                return 201, service.draft(self.body())
            if method == "POST" and path == "/v1/drafts/from-link":
                return 201, service.from_link(self.body())
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
                    return 200, service.remote(ident, "status" if action == "remote" else action)
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

        def respond(self):
            try:
                code, value = self.dispatch()
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
        do_OPTIONS = respond

    return ThreadingHTTPServer((host or service.c.host, service.c.port if port is None else port), Handler)

"""HTTPS con IP pública fijada al socket, allowlist exacta, sin redirects/proxies."""
import http.client
import ipaddress
import json
import socket
import ssl
from urllib.parse import urlsplit
from .validation import Problem, https, require


def resolve_public(url, allowed_hosts):
    https(url, "asset URL")
    u = urlsplit(url)
    host = u.hostname.encode("idna").decode("ascii").lower()
    require(host in allowed_hosts, "Dominio de archivo no autorizado en ASSET_ALLOWED_HOSTS")
    try:
        addresses = list(dict.fromkeys(x[4][0] for x in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)))
    except OSError:
        raise Problem("No se pudo resolver el dominio del archivo", 422, "ASSET_DNS")
    require(bool(addresses) and all(ipaddress.ip_address(ip).is_global for ip in addresses), "El archivo debe estar en una IP pública")
    return host, addresses[0]


class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, ip):
        super().__init__(host, timeout=30, context=ssl.create_default_context())
        self.ip = ip

    def connect(self):
        raw = socket.create_connection((self.ip, 443), self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


def fetch(url, hosts, limit=10 * 1024 * 1024, json_file=False):
    host, ip = resolve_public(url, hosts)
    u = urlsplit(url)
    path = u.path or "/"
    if u.query:
        path += "?" + u.query
    conn = PinnedHTTPS(host, ip)
    try:
        conn.request("GET", path, headers={"User-Agent": "OrbitaPublisher/1.0", "Accept-Encoding": "identity"})
        r = conn.getresponse()
        require(r.status == 200, "El archivo debe responder 200 sin redirecciones ni autenticación")
        size = r.getheader("Content-Length")
        if size is not None:
            require(size.isdigit() and int(size) <= limit, "Archivo demasiado grande")
        data = r.read(limit + 1)
        require(len(data) <= limit and bool(data), "Archivo vacío o demasiado grande")
        if json_file:
            try:
                return json.loads(data)
            except (ValueError, UnicodeError):
                raise Problem("El manifiesto no es JSON válido")
        require(data.startswith(b"\x89PNG\r\n\x1a\n") or data.startswith(b"\xff\xd8\xff"), "Solo JPG/PNG real; no HTML ni SVG")
        return data
    except (OSError, http.client.HTTPException):
        raise Problem("No se pudo descargar el archivo", 422, "ASSET_DOWNLOAD")
    finally:
        conn.close()

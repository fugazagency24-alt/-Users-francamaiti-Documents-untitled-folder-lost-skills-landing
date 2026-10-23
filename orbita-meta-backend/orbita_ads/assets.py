"""HTTPS con IP pública fijada al socket, allowlist exacta, sin redirects/proxies."""
import http.client
import ipaddress
import json
import re
import socket
import ssl
import struct
from urllib.parse import urlsplit
from .validation import Problem, https, require

# Enlaces que la gente suele pegar pero que NO son el archivo: carpetas, visores y páginas de descarga.
NOT_A_FILE = [
    (r"(^|\.)drive\.google\.com$", r"/drive/folders/", "Es una carpeta de Google Drive, no un archivo. Subí el archivo a Orbita o pegá su enlace directo."),
    (r"(^|\.)drive\.google\.com$", r"/(file/d/|open)", "Es la página de vista previa de Google Drive, no el archivo. Subilo a Orbita o usá un enlace directo de tu almacenamiento."),
    (r"(^|\.)docs\.google\.com$", r"", "Es un documento de Google, no un archivo de imagen o video."),
    (r"(^|\.)dropbox\.com$", r"", "Es una página de Dropbox. Subí el archivo a Orbita o usá un enlace directo de tu almacenamiento."),
    (r"(^|\.)(wetransfer\.com|we\.tl|mega\.nz|mediafire\.com)$", r"", "Es una página de descarga, no el archivo directo."),
    (r"(^|\.)(youtube\.com|youtu\.be|vimeo\.com|tiktok\.com|instagram\.com|facebook\.com|fb\.watch)$", r"", "Es una página de una red social o reproductor, no el archivo del video."),
    (r"(^|\.)canva\.com$", r"", "Es un diseño de Canva. Exportalo como JPG/PNG/MP4 y subilo a Orbita."),
]


def not_a_file_reason(url):
    u = urlsplit(url)
    host, path = (u.hostname or "").lower(), u.path or "/"
    for host_re, path_re, reason in NOT_A_FILE:
        if re.search(host_re, host) and re.search(path_re, path):
            return reason
    return None


def resolve_public(url, allowed_hosts):
    https(url, "asset URL")
    reason = not_a_file_reason(url)
    if reason:
        raise Problem(reason, 422, "NOT_A_DIRECT_FILE")
    u = urlsplit(url)
    host = u.hostname.encode("idna").decode("ascii").lower()
    require("*" in allowed_hosts or host in allowed_hosts, f"Dominio de archivo no autorizado: {host}. Agregalo a ASSET_ALLOWED_HOSTS")
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


def fetch(url, hosts, limit=10 * 1024 * 1024, json_file=False, first_bytes=None):
    host, ip = resolve_public(url, hosts)
    u = urlsplit(url)
    path = u.path or "/"
    if u.query:
        path += "?" + u.query
    conn = PinnedHTTPS(host, ip)
    try:
        headers = {"User-Agent": "OrbitaPublisher/1.0", "Accept-Encoding": "identity"}
        if first_bytes:
            headers["Range"] = f"bytes=0-{first_bytes - 1}"
        conn.request("GET", path, headers=headers)
        r = conn.getresponse()
        if first_bytes:
            require(r.status in (200, 206), "El archivo debe responder sin redirecciones ni autenticación")
            return r.getheader("Content-Type", ""), r.read(first_bytes)
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


def image_size(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return "PNG", *struct.unpack(">II", data[16:24])
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            break
        marker, length = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return "JPG", w, h
        i += 2 + length
    return "JPG", None, None


def probe(url, hosts, kind):
    """Comprueba que el enlace sea el archivo publicitario directo, antes de armar el borrador."""
    if kind == "image":
        fmt, width, height = image_size(fetch(url, hosts))
        return {"ok": True, "kind": "image", "format": fmt, "width": width, "height": height}
    content_type, head = fetch(url, hosts, first_bytes=64)
    require(not head.lstrip().startswith(b"<") and "html" not in content_type.lower(),
            "El enlace devuelve una página web, no el archivo del video")
    if head[4:8] == b"ftyp":
        fmt = "MOV" if head[8:10] == b"qt" else "MP4"
    elif head.startswith(b"\x1aE\xdf\xa3"):
        fmt = "WEBM/MKV"
    elif head.startswith(b"RIFF") and head[8:12] == b"AVI ":
        fmt = "AVI"
    else:
        raise Problem("No se reconoce como video (MP4/MOV/WEBM/AVI)", 422, "ASSET_FORMAT")
    return {"ok": True, "kind": "video", "format": fmt,
            "note": "Meta descarga el video desde este enlace: debe seguir accesible hasta que termine el procesamiento."}

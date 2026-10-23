import fcntl
import os
import secrets
import sys
import threading
import webbrowser
from pathlib import Path
from .config import Config
from .service import Service
from .server import make_server


def local_defaults():
    """Uso local: datos en ~/.orbita-meta-ads y clave de servicio generada una vez, sin pedir nada."""
    data = Path(os.environ.setdefault("ORBITA_DB", str(Path.home() / ".orbita-meta-ads" / "orbita.sqlite3"))).parent
    data.mkdir(parents=True, exist_ok=True)
    # Enlaces pegados de cualquier host HTTPS público; la protección por IP pública fijada sigue activa.
    os.environ.setdefault("ASSET_ALLOWED_HOSTS", "*")
    if not os.environ.get("ORBITA_SERVICE_KEY"):
        key_file = data / "service_key"
        if not key_file.exists():
            fd = os.open(key_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as f:
                f.write(secrets.token_urlsafe(48))
        os.environ["ORBITA_SERVICE_KEY"] = key_file.read_text().strip()


def main():
    os.umask(0o077)
    local_defaults()
    config = Config.from_env()
    Path(config.db_path).parent.mkdir(parents=True, exist_ok=True)
    # Linux/macOS; Windows use the provided Dockerfile.
    lockfile = open(config.db_path + ".lock", "a")
    try:
        fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("Ya hay un Orbita Meta Ads abierto con estos datos. Usá esa ventana o cerrala primero.")
    service = Service(config)
    service.store.recover()
    server = make_server(service)
    worker = threading.Thread(target=service.worker, daemon=True)
    worker.start()
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"Orbita · Meta Ads listo en {url}  (modo {'SIMULACIÓN' if service.c.mode == 'mock' else 'REAL'})", flush=True)
    print(f"Datos: {Path(config.db_path).parent}  ·  Cerrar: Ctrl+C", flush=True)
    if "--open" in sys.argv:
        threading.Timer(0.8, webbrowser.open, (url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        service.stop.set()
        server.server_close()
        worker.join(timeout=65)
        # Keep lock until process exit, including any in-flight worker operation.
        if worker.is_alive():
            worker.join()
        lockfile.close()


if __name__ == "__main__":
    main()

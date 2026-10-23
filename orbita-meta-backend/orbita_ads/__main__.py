import fcntl
import os
import threading
from pathlib import Path
from .config import Config
from .service import Service
from .server import make_server


def main():
    os.umask(0o077)
    config = Config.from_env()
    Path(config.db_path).parent.mkdir(parents=True, exist_ok=True)
    # Linux/macOS; Windows use the provided Dockerfile.
    lockfile = open(config.db_path + ".lock", "a")
    try:
        fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("Ya existe un proceso Orbita usando esta base de datos")
    service = Service(config)
    service.store.recover()
    server = make_server(service)
    worker = threading.Thread(target=service.worker, daemon=True)
    worker.start()
    print(f"Orbita Publisher {config.mode}: http://{config.host}:{config.port} (solo backend interno)", flush=True)
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

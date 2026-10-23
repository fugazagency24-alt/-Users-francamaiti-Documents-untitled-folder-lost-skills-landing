import os
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    api_key: str
    db_path: str = "data/orbita.sqlite3"
    mode: str = "mock"
    meta_token: str = ""
    meta_app_secret: str = ""
    graph_version: str = "v26.0"
    asset_hosts: tuple[str, ...] = ()
    live_enabled: bool = False
    meta_use_env_proxy: bool = False
    host: str = "127.0.0.1"
    port: int = 8787

    @classmethod
    def from_env(cls):
        c = cls(
            api_key=os.getenv("ORBITA_SERVICE_KEY", ""),
            db_path=os.getenv("ORBITA_DB", "data/orbita.sqlite3"),
            mode=os.getenv("META_MODE", "mock"),
            meta_token=os.getenv("META_ACCESS_TOKEN", ""),
            meta_app_secret=os.getenv("META_APP_SECRET", ""),
            graph_version=os.getenv("META_GRAPH_VERSION", "v26.0"),
            asset_hosts=tuple(x.strip().lower() for x in os.getenv("ASSET_ALLOWED_HOSTS", "").split(",") if x.strip()),
            live_enabled=os.getenv("ENABLE_LIVE_PUBLISH", "false").lower() == "true",
            meta_use_env_proxy=os.getenv("META_USE_ENV_PROXY", "false").lower() == "true",
            host=os.getenv("HOST", "127.0.0.1"),
            port=int(os.getenv("PORT", "8787")),
        )
        if len(c.api_key) < 32:
            raise ValueError("ORBITA_SERVICE_KEY debe tener al menos 32 caracteres aleatorios")
        if c.mode not in ("mock", "live"):
            raise ValueError("META_MODE debe ser mock o live")
        if not re.fullmatch(r"v\d+\.0", c.graph_version):
            raise ValueError("Versión Graph inválida")
        if "*" in c.asset_hosts and len(c.asset_hosts) > 1:
            raise ValueError("ASSET_ALLOWED_HOSTS: usá * solo o una lista de hosts exactos")
        if c.mode == "live" and not c.meta_token:
            raise ValueError("Falta META_ACCESS_TOKEN")
        return c

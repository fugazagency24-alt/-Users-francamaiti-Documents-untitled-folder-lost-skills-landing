"""Secretos del servidor local. Se guardan en un archivo 0600 fuera de Git y nunca se devuelven al navegador."""
import json
import os
import re
import threading
from pathlib import Path
from .validation import Problem, require

SECRETS = {
    "meta_access_token": ("META_ACCESS_TOKEN", re.compile(r"[A-Za-z0-9_\-.|]{20,1000}"), "token de Meta"),
    "meta_app_secret": ("META_APP_SECRET", re.compile(r"[a-f0-9]{32}"), "clave secreta de la app (32 caracteres hex)"),
    "anthropic_api_key": ("ANTHROPIC_API_KEY", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,300}"), "API key de Anthropic (sk-ant-...)"),
}


class Secrets:
    def __init__(self, path):
        self.path = Path(path)
        self.lock = threading.Lock()

    def _read(self):
        try:
            return json.loads(self.path.read_text())
        except FileNotFoundError:
            return {}

    def _write(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        os.chmod(tmp, 0o600)
        os.replace(tmp, self.path)

    def get(self, name):
        env = os.environ.get(SECRETS[name][0], "")
        return env or self._read().get(name, "")

    def set(self, name, value):
        require(name in SECRETS, "Secreto desconocido")
        value = value.strip() if isinstance(value, str) else ""
        require(bool(SECRETS[name][1].fullmatch(value)), f"Formato inválido para {SECRETS[name][2]}")
        if os.environ.get(SECRETS[name][0]):
            raise Problem(f"{SECRETS[name][0]} está definido como variable de entorno; cambialo ahí", 409)
        with self.lock:
            data = self._read()
            data[name] = value
            self._write(data)

    def clear(self, name):
        require(name in SECRETS, "Secreto desconocido")
        with self.lock:
            data = self._read()
            data.pop(name, None)
            self._write(data)

    def status(self):
        """Solo si está cargado y de dónde; nunca el valor ni fragmentos."""
        data = self._read()
        return {name: {"configured": bool(os.environ.get(env) or data.get(name)),
                       "source": "env" if os.environ.get(env) else ("servidor" if data.get(name) else None)}
                for name, (env, _, _) in SECRETS.items()}

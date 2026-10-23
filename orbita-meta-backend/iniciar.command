#!/bin/bash
# Orbita · Meta Ads en tu computadora. macOS: doble clic. Linux/macOS por terminal: ./iniciar.command
# La primera vez prepara Python y la librería de la IA; después solo abre la pantalla.
set -e
cd "$(dirname "$0")"

PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$(command -v "$c")"; break
  fi
done

if [ -z "$PY" ]; then
  UV="$(command -v uv || true)"
  [ -z "$UV" ] && [ -x "$HOME/.local/bin/uv" ] && UV="$HOME/.local/bin/uv"
  if [ -z "$UV" ]; then
    echo "Hace falta Python 3.10 o más nuevo."
    read -r -p "¿Lo instalo con uv (instalador oficial de Astral, solo para tu usuario)? [S/n] " r
    case "$r" in
      n|N) echo "Instalá Python desde https://www.python.org/downloads/ y volvé a abrir este archivo."; exit 1 ;;
    esac
    curl -LsSf https://astral.sh/uv/install.sh | sh
    UV="$HOME/.local/bin/uv"
  fi
  "$UV" python install 3.12
  PY="$("$UV" python find 3.12)"
fi

if [ ! -x .venv/bin/python ]; then
  echo "Preparando el entorno (solo la primera vez)…"
  "$PY" -m venv .venv
fi
.venv/bin/python -m pip install -q --disable-pip-version-check -r requirements.txt

exec .venv/bin/python -m orbita_ads --open

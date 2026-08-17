#!/usr/bin/env sh
set -e

echo "[INFO] Starting FastAPI..."

RELOAD=""

if [ "${ENV:-prod}" = "dev" ]; then
    echo "[INFO] Development mode: enabling reload"
    RELOAD="--reload"
fi

exec /app/.venv/bin/uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  $RELOAD
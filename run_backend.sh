#!/bin/bash

# Start Backend Server
echo "Starting RAG Healthcare Assistant Backend"

cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

.venv/bin/pip install -r backend/requirements.txt

echo "Backend on http://localhost:8000"
echo "Docs on http://localhost:8000/docs"

exec .venv/bin/uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

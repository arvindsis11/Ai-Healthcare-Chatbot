#!/bin/bash

set -e

echo "AI Healthcare Chatbot setup"

cd "$(dirname "$0")" || exit 1

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r backend/requirements.txt

cd frontend
npm install
cd ..

echo "Setup complete"
echo "Run backend with ./run_backend.sh"
echo "Run frontend with ./run_frontend.sh"

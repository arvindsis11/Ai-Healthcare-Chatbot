#!/bin/bash
set -euo pipefail
# Local test runner for the Ai-Healthcare-Chatbot project

echo "--- Running Backend Tests ---"
export PYTHONPATH=./backend
pytest tests/ backend/tests/

echo ""
echo "--- Running Frontend Tests ---"
(cd frontend && npm run test -- --ci --passWithNoTests)

echo ""
echo "Tests completed!"

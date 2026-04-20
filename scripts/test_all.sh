#!/bin/bash
# Local test runner for the Ai-Healthcare-Chatbot project

echo "--- Running Backend Tests ---"
PYTHONPATH=./backend pytest tests/ backend/tests/

echo ""
echo "--- Running Frontend Tests ---"
cd frontend
npm run test -- --ci --passWithNoTests
cd ..

echo ""
echo "Tests completed!"

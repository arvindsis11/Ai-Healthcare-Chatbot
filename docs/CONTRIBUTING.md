# Contributing Guide

Thanks for contributing to the AI Healthcare Platform!

Please read and follow our [Code of Conduct](../CODE_OF_CONDUCT.md) to keep this community
welcoming for everyone.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.11+** — [python.org](https://www.python.org/downloads/)
- **Node.js 20+** — [nodejs.org](https://nodejs.org/)
- **Docker 24+** (optional, for full-stack local testing) — [docker.com](https://www.docker.com/)
- **Git** — [git-scm.com](https://git-scm.com/)

## Development Flow

1. Fork and create a branch from `master`.
2. Keep changes incremental and runnable.
3. Run backend and frontend locally before opening PR.
4. Add/update tests when changing behavior.
5. Update docs when architecture or APIs change.

## Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install backend dependencies (production + dev/test)
pip install -r backend/requirements.txt -r backend/requirements-dev.txt

# Download the spaCy English model (required for symptom extraction)
python -m spacy download en_core_web_sm

# Configure environment variables
cp .env.example .env
# Edit .env — set OPENAI_API_KEY for OpenAI, or configure a local LLM
# (LM Studio / Ollama) — see docs/SETUP.md for details

# Seed the ChromaDB knowledge base
python scripts/ingest_data.py

# Start the backend server (http://localhost:8000)
./run_backend.sh
```

## Frontend Setup

```bash
# Install Node.js dependencies
cd frontend
npm install

# Return to the repo root and start the dev server (http://localhost:3000)
cd ..
./run_frontend.sh
```

## Running Tests

### Backend

```bash
# Activate the virtual environment first
source .venv/bin/activate

# Run all backend tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=backend --cov-report=term-missing
```

### Frontend

```bash
cd frontend
npm test          # Run all Jest tests once
npm run test:watch  # Watch mode for TDD
```

## Linting

### Backend

```bash
# Check for lint errors
ruff check backend

# Auto-fix where possible
ruff check backend --fix
```

### Frontend

```bash
cd frontend
npm run lint
```

## Local Verification

```bash
./run_backend.sh
./run_frontend.sh
```

Backend smoke tests:

```bash
curl http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I have a headache and fever"}'
```

## Code Standards

- **Python**: typed, modular, small functions, PEP 8 via `ruff`.
- **TypeScript**: avoid `any`, prefer explicit interfaces, ESLint enforced.
- Keep API calls in `frontend/src/services`.
- Keep backend domain logic in `backend/app/services`.
- Never commit secrets — use `.env` (gitignored).

## Pull Request Checklist

- [ ] App runs locally
- [ ] No broken imports or stale paths
- [ ] Tests updated/passing where applicable
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] `ruff check backend` passes with no errors
- [ ] `npm run lint` passes with no errors


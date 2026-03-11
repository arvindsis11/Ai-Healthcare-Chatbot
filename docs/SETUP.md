# Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 20+
- npm 10+
- Docker + Docker Compose (for full stack runtime)

## Local Development

1. Install dependencies:

```bash
./setup.sh
```

2. Start backend:

```bash
./run_backend.sh
```

3. Start frontend:

```bash
./run_frontend.sh
```

## Environment Variables

Create `backend/.env`:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/healthcare
REDIS_URL=redis://localhost:6379/0
RATE_LIMIT_PER_MINUTE=60
REQUEST_SIZE_LIMIT_BYTES=65536
```

If `OPENAI_API_KEY` is unset, backend returns fallback guidance responses.

## Containerized Full Stack

```bash
docker compose up --build
```

Services started:

- backend (`:8000`)
- frontend (`:3000`)
- redis (`:6379`)
- postgres (`:5432`)
- nginx (`:80`)

## Data Ingestion

```bash
python scripts/ingest_data.py
```

## CI Validation Locally

```bash
pytest tests/
cd frontend && npm run lint && npm run build
```

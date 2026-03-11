# Setup Guide

This guide covers the current supported runtime: FastAPI backend + Next.js frontend.

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm 9+

## Install

```bash
./setup.sh
```

## Run Backend

```bash
./run_backend.sh
```

Backend endpoints:
- `http://localhost:8000`
- `http://localhost:8000/docs`

## Run Frontend

```bash
./run_frontend.sh
```

Frontend URL:
- `http://localhost:3000`

## Run Full Stack

```bash
./start.sh
```

## Ingest Data

```bash
python scripts/ingest_data.py
```

## Environment Variables

Create `backend/.env` as needed:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo
```

If `OPENAI_API_KEY` is empty, backend runs in fallback response mode.

## Troubleshooting

### Backend does not start
- Ensure `.venv` exists and dependencies installed by `setup.sh`.
- Verify port `8000` is free.

### Frontend cannot reach backend
- Confirm backend is running on port `8000`.
- Verify rewrite config in `frontend/next.config.js`.

### Slow first query
- First query may load embedding models and can take longer.

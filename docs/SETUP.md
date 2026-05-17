# Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 20+
- npm 10+
- Docker + Docker Compose (for full stack runtime)

---

## Quick Start (Docker)

The easiest way to run the full stack is with Docker Compose:

```bash
cp .env.example .env
# Edit .env — see Environment Variables below
docker compose up --build
```

Services started:

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |
| NGINX (reverse proxy) | http://localhost:80 |

---

## Local Development (without Docker)

1. Install dependencies:

```bash
./setup.sh
```

2. Start backend:

```bash
./run_backend.sh
```

3. Start frontend (new terminal):

```bash
./run_frontend.sh
```

---

## Environment Variables

Copy the template and edit it:

```bash
cp .env.example .env
```

### LLM Provider

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `openai` | Which LLM backend to use: `openai`, `lm-studio`, or `ollama` |
| `OPENAI_API_KEY` | _(empty)_ | Required when `LLM_PROVIDER=openai`. Not needed for local providers. |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Model name passed to the LLM server. |
| `OPENAI_BASE_URL` | _(empty)_ | Base URL for local providers. Leave blank to use the provider default. |
| `LLM_TIMEOUT_SECONDS` | `0` | Request timeout for LLM calls. `0` uses the provider default (30s for OpenAI, 120s for local providers). |

If `OPENAI_API_KEY` is unset and `LLM_PROVIDER=openai`, the backend runs in fallback mode and returns static guidance responses without calling any LLM.

### Other variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | _(empty)_ | PostgreSQL connection string. Falls back to in-memory store if unset. |
| `REDIS_URL` | _(empty)_ | Redis connection string. Falls back to in-memory cache if unset. |
| `CACHE_TTL_SECONDS` | `300` | How long query results are cached (seconds). |
| `RATE_LIMIT_PER_MINUTE` | `60` | Max API requests per IP per minute. |
| `REQUEST_SIZE_LIMIT_BYTES` | `65536` | Max HTTP request body size (64 KB). |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated list of CORS-allowed origins. |
| `DEBUG` | `false` | Enable verbose error messages and auto-reload. |

---

## Local LLM Setup (LM Studio / Ollama)

You can run the app entirely offline and without an OpenAI API key by using a local LLM server. Both LM Studio and Ollama expose an OpenAI-compatible API, so no other code changes are needed.

### LM Studio

1. Download and install [LM Studio](https://lmstudio.ai)
2. Search for and download a model inside the app (e.g. `deepseek-r1-distill-llama-8b`)
3. Open the **Local Server** tab and click **Start Server** (default port: `1234`)
4. Set these variables in your `.env`:

```env
LLM_PROVIDER=lm-studio
OPENAI_MODEL=deepseek-r1-distill-llama-8b
OPENAI_BASE_URL=http://localhost:1234/v1
```

### Ollama

1. Download and install [Ollama](https://ollama.com)
2. Pull a model:

```bash
ollama pull llama3
```

3. Ollama starts its server automatically on port `11434`
4. Set these variables in your `.env`:

```env
LLM_PROVIDER=ollama
OPENAI_MODEL=llama3
OPENAI_BASE_URL=http://localhost:11434/v1
```

### Docker networking

When running inside Docker, the backend container cannot reach `localhost` on the host machine. Use `host.docker.internal` as the hostname instead:

```env
# LM Studio
OPENAI_BASE_URL=http://host.docker.internal:1234/v1

# Ollama
OPENAI_BASE_URL=http://host.docker.internal:11434/v1
```

This works automatically on Windows and macOS with Docker Desktop. On Linux, `docker-compose.yml` already adds the required `extra_hosts` entry so `host.docker.internal` resolves correctly.

### Startup validation

When `LLM_PROVIDER` is set to `lm-studio` or `ollama`, the backend pings the server on startup. If it is unreachable, a clear warning is logged — so you know immediately if the LLM server needs to be started.

### Latency and timeouts

Local models are significantly slower than the OpenAI API — first inference can take 30–60+ seconds depending on hardware. The backend applies a per-provider request timeout to surface errors quickly rather than hanging silently:

| Provider | Default timeout |
|---|---|
| `openai` | 30s |
| `lm-studio` | 120s |
| `ollama` | 120s |

Override with `LLM_TIMEOUT_SECONDS` in your `.env` if your hardware needs more or less time.

---

## Data Ingestion

```bash
python scripts/ingest_data.py
```

---

## Running Tests

```bash
pytest tests/
```

Frontend checks:

```bash
cd frontend && npm run lint && npm run build
```

# Enterprise Architecture

## Layered Runtime Design

```text
Frontend (Next.js)
  -> API Layer (FastAPI routes)
  -> Service Layer (chat orchestration, triage, multilingual)
  -> RAG Layer (semantic retrieval + reranking + citation assembly)
  -> Repository Layer (ChromaDB, session persistence abstraction)
  -> Infrastructure Layer (Redis, PostgreSQL, NGINX)
```

## Backend Structure

```text
backend/app/
  api/            # route handlers only
  services/       # business logic and orchestration
  repositories/   # vector db + session persistence abstraction
  rag/            # ingestion and text processing
  ai/             # prompt guard + translation services
  middleware/     # request id, latency, rate limiting, size limits
  models/         # request/response schemas
  core/           # settings, dependency wiring, logging
  main.py         # app bootstrap
```

## Frontend Structure

```text
frontend/src/
  app/
  features/
    chat/
    analytics/
    admin/
  components/
  hooks/
  services/
  store/
  types/
```

## Request Lifecycle (`POST /api/v1/chat`)

1. API validates request payload.
2. Prompt guard blocks unsafe jailbreak-like input patterns.
3. Language detection and normalization executed.
4. Symptom extraction and rule-based triage generated.
5. Cache lookup (`chat:{sha256(query)}`) attempted.
6. On miss, hybrid RAG retrieval and reranking execute.
7. LLM response generated with context + symptom analysis.
8. Session repository stores user and assistant messages.
9. Response includes citations, triage output, specialist recommendation, disclaimer.

## Observability

- Structured JSON logging.
- Request ID propagation in headers.
- Latency headers (`X-Latency-MS`) and request-level logs.

## Safety and Compliance Baseline

- Medical non-diagnostic guardrails in prompts and API disclaimer.
- Input validation with Pydantic.
- Configurable CORS allow-list.
- Basic abuse controls (rate limiting and body size limit).

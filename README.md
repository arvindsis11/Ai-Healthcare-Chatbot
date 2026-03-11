# AI Healthcare Chatbot

AI Healthcare Chatbot is a FastAPI + Next.js Retrieval-Augmented Generation (RAG) application for general healthcare guidance.

## Runtime Scope

- Backend: FastAPI API under `backend/app`
- Frontend: Next.js App Router under `frontend/src`
- Retrieval: ChromaDB + SentenceTransformers
- LLM orchestration: LangChain + OpenAI (with fallback mode when key is absent)

Medical disclaimer: This system provides general educational information and is not a substitute for professional medical advice.

## Quick Start

```bash
./setup.sh
./run_backend.sh
./run_frontend.sh
```

- Backend: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

## Current API Endpoints

- `GET /` - API root metadata
- `GET /api/v1/health` - health status
- `POST /api/v1/chat` - main chat endpoint
- `POST /api/v1/analyze-symptoms` - symptom-first analysis endpoint

## Folder Structure

```text
backend/
        app/
                api/
                services/
                repositories/
                models/
                rag/
                core/
        requirements.txt

frontend/
        src/
                app/
                components/
                services/
                hooks/
                store/
                styles/
        package.json
```

## Development Notes

- Frontend calls `/api/v1/*`; Next.js rewrites `/api/*` to backend in local dev.
- Vector data is persisted under `embeddings/`.
- Run ingestion with `python scripts/ingest_data.py`.

## License

MIT

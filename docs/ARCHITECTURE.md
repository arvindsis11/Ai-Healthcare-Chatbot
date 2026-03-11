# System Architecture

This document describes the current runtime architecture of the repository.

## High-Level Architecture

```text
Next.js Frontend (frontend/src)
  -> /api/v1/* requests
Next.js rewrite proxy (frontend/next.config.js)
  -> FastAPI Backend (backend/app)
FastAPI Services
  -> RAG service
  -> LLM service
  -> Vector repository (ChromaDB)
```

## Backend Layout

```text
backend/app/
  api/
    chat.py
  services/
    rag_service.py
    llm_service.py
  repositories/
    vector_db.py
  models/
    chat.py
  rag/
    data_ingestion.py
    text_processing.py
  core/
    settings.py
  main.py
```

### Request Flow

```text
POST /api/v1/chat
 -> api/chat.py
 -> services/rag_service.py
 -> repositories/vector_db.py (similarity retrieval)
 -> services/llm_service.py (response + triage)
 -> response model
```

## Frontend Layout

```text
frontend/src/
  app/
    layout.tsx
    page.tsx
  components/
    ChatWindow.tsx
    Sidebar.tsx
    MessageBubble.tsx
    InputBar.tsx
  services/
    chatService.ts
  hooks/
  store/
  styles/
    globals.css
```

### UI Flow

```text
ChatWindow
 -> sends message via services/chatService.ts
 -> backend /api/v1/chat
 -> renders messages, risk badges, and sources
```

## Data and Ingestion Flow

```text
data/*.yml
 -> rag/text_processing.py
 -> rag/data_ingestion.py
 -> repositories/vector_db.py
 -> embeddings/chroma.sqlite3
```

## Security and Safety Baseline

- Input validation with Pydantic models
- CORS restrictions configured in `core/settings.py`
- Medical disclaimer embedded in API responses and frontend banner
- No diagnosis claims in prompts

## Current Non-Goals

- No legacy Flask/ChatterBot runtime paths
- No active voice endpoint in backend
- No separate Docker topology in this repository snapshot

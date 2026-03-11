# PROJECT ANALYSIS

## 1. Project Overview

### Purpose
Ai-Healthcare-Chatbot is a healthcare-focused conversational assistant repository that currently contains a modern FastAPI + Next.js RAG chatbot implementation and artifacts/docs for older chatbot variants.

### Project Type
- AI-enabled full-stack web application
- Healthcare information assistant (not diagnostic)
- Retrieval-Augmented Generation (RAG) system using vector search + LLM responses

### Problem It Solves
- Provides users with general healthcare guidance in conversational form
- Adds symptom extraction, triage-style risk signaling, and source-backed response context
- Offers a simpler frontend experience for non-technical users to interact with a healthcare knowledge base

### Main Features (Current Runtime)
- Chat API with symptom-aware response generation
- Vector retrieval from YAML-based healthcare corpus via ChromaDB
- Symptom extraction + structured triage metadata (`low|medium|high`)
- Next.js chat UI with modern layout, sidebar, sticky input, dark mode, loading/typing states
- API rewrite from frontend to backend for local dev (`/api/*` -> backend)

### Target Users
- End users seeking general healthcare information
- Developers/students exploring AI healthcare assistant patterns
- Contributors interested in open-source RAG chatbot architecture

---

## 2. Technology Stack

### Backend
- Python 3.12 runtime (dev container), app intended for Python 3.8+
- FastAPI (`backend/main.py`) for HTTP API
- Pydantic + pydantic-settings for schema/config (`backend/models/chat.py`, `backend/config/settings.py`)
- Uvicorn for ASGI serving (`run_backend.sh`)

Why used:
- Async-capable API framework, typed validation, rapid endpoint development.

### Frontend
- Next.js 14 App Router (`frontend/app/*`)
- React + TypeScript (`frontend/components/*`, `frontend/hooks/*`)
- Tailwind CSS (`frontend/styles/globals.css`, `frontend/tailwind.config.js`)
- Lucide icons (`frontend/package.json`, components)

Why used:
- Rapid full-stack React app development with modern component UX and utility-first styling.

### AI / ML
- LangChain (`backend/services/llm_service.py`) for prompt chains
- OpenAI Chat model via `langchain-openai` (conditional by key presence)
- SentenceTransformers `all-MiniLM-L6-v2` for embedding generation (`backend/services/vector_db.py`)

Why used:
- LangChain simplifies prompt orchestration; SentenceTransformers gives local semantic embeddings.

### Vector Database
- ChromaDB persistent client (`backend/services/vector_db.py`)
- Storage in `embeddings/chroma.sqlite3`

Why used:
- Lightweight local vector DB with persistence and metadata search.

### Voice AI
- Documented in `docs/AI_MODEL.md` and `docs/ARCHITECTURE.md` (Whisper + ElevenLabs)
- Not implemented in current runtime backend codebase (no `voice_service.py` present)

Why listed:
- Represents legacy/planned architecture, not active implementation.

### DevOps / Tooling
- Bash startup scripts (`setup.sh`, `run_backend.sh`, `run_frontend.sh`, `start.sh`)
- Next.js rewrite proxy (`frontend/next.config.js`)
- VS Code Flask launch config (`.vscode/launch.json`)

### Testing
- Pytest-style tests in `tests/test_backend.py`
- No frontend test suite present

---

## 3. Repository Structure

```text
Ai-Healthcare-Chatbot/
├── .github/
│   ├── copilot-instructions.md
│   └── prompts/project-architecture.md
├── .vscode/
│   └── launch.json
├── backend/
│   ├── api/chat.py
│   ├── config/settings.py
│   ├── models/chat.py
│   ├── rag/data_ingestion.py
│   ├── services/{llm_service.py, rag_service.py, vector_db.py}
│   ├── utils/text_processing.py
│   ├── main.py
│   └── requirements.txt
├── data/
│   ├── botprofile.yml
│   ├── cough.cold.yml
│   ├── doctor.yml
│   ├── fever.yml
│   ├── fracture.yml
│   ├── generalhealth.yml
│   ├── greetings.yml
│   ├── headache.yml
│   ├── new.yml
│   └── personalinfo.yml
├── docs/
│   ├── AI_MODEL.md
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   ├── ROADMAP.md
│   └── SETUP.md
├── embeddings/
│   └── chroma.sqlite3
├── frontend/
│   ├── app/{layout.tsx,page.tsx}
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── InputBar.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ChatInterface.tsx (legacy)
│   │   ├── ChatInput.tsx (legacy)
│   │   └── SymptomAnalysis.tsx (legacy)
│   ├── hooks/useChat.ts
│   ├── styles/globals.css
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   └── next-env.d.ts
├── scripts/ingest_data.py
├── tests/test_backend.py
├── README.md
├── requirements.txt
├── setup.sh
├── start.sh
├── run_backend.sh
└── run_frontend.sh
```

### Responsibility by Folder
- `backend/`: Active API, orchestration, retrieval, model schemas.
- `frontend/`: Active UI and user interaction layer.
- `data/`: Domain conversation corpora used for ingestion.
- `scripts/`: Utility ingestion runner.
- `docs/`: Architectural intent and contributor onboarding.
- `embeddings/`: Persisted vector index.
- `.github/`: AI coding governance + architecture prompt template.

---

## 4. Backend Architecture

### FastAPI Structure
- App bootstrap: `backend/main.py`
- Router registration: `app.include_router(chat_router, prefix="/api/v1")`
- CORS middleware from `settings.allowed_origins`

### API Layer
- `backend/api/chat.py`
- Endpoints: `/chat`, `/analyze-symptoms`, `/health` under `/api/v1`
- Uses dependency provider `get_rag_service()` with module-level singleton

### Service Layer
- `RAGService` (`backend/services/rag_service.py`)
  - Symptom extraction via keyword + regex
  - Retrieval call to vector DB
  - Response generation via LLM service
- `LLMService` (`backend/services/llm_service.py`)
  - Prompt templates for medical response + symptom analysis
  - LLM call path if API key configured
  - Fallback deterministic response mode when key absent
- `VectorDatabase` (`backend/services/vector_db.py`)
  - Chroma persistent client
  - SentenceTransformer embedding generation
  - add/search/get/clear operations

### Model Layer
- `backend/models/chat.py`
- Pydantic request/response and triage enums (`RiskLevel`)

### RAG Pipeline
Flow implemented:

```text
User request
 -> FastAPI route (/api/v1/chat)
 -> RAGService.query_with_symptoms()
 -> symptom extraction (keywords/regex)
 -> LLMService.analyze_symptoms()
 -> VectorDatabase.search() (embedding + similarity query)
 -> LLMService.generate_medical_response(context + triage)
 -> ChatResponse (response + sources + symptom_analysis)
```

### Vector DB Usage
- Collection created/get by name (`healthcare_docs` default)
- Embeddings computed on ingest and query-time
- Sources returned from metadata for citation display

### Observed Backend Design Notes
- Service singleton in router is convenient but tightly coupled
- Broad `except` blocks hide error granularity
- API startup now resilient without OpenAI key (fallback mode)

---

## 5. Frontend Architecture

### Next.js Structure
- App Router with root layout/page (`frontend/app/layout.tsx`, `frontend/app/page.tsx`)
- Main UI component: `ChatWindow.tsx`

### Component Hierarchy (Current)

```text
page.tsx
 -> ChatWindow
    -> Sidebar
    -> MessageBubble (n)
    -> InputBar
```

### State Management
- Local component state in `ChatWindow.tsx`
  - messages, loading state, theme state, mobile sidebar state, streaming simulation state
- Legacy `useChat` hook exists (`frontend/hooks/useChat.ts`) but not wired to current page

### API Integration
- Frontend calls `/api/v1/chat`
- Next rewrite in `frontend/next.config.js` maps `/api/*` to backend `http://localhost:8000/api/*`
- No `frontend/app/api/chat/route.ts` currently exists (despite docs claiming it)

### UI Features (Current)
- Full-height split layout
- Mobile-collapsible sidebar
- Persistent theme toggle via `localStorage`
- Medical disclaimer banner
- Sticky autosizing input with Enter/Shift+Enter behavior
- Web Speech API mic capture (browser-dependent)
- Message copy + regenerate controls
- Risk badges and sources display
- Simulated streaming reveal and typing indicator

### Legacy Frontend Artifacts
- `ChatInterface.tsx`, `ChatInput.tsx`, `SymptomAnalysis.tsx`, `useChat.ts`, and older utility classes in `globals.css` remain in repo but are not used by current page route.

---

## 6. AI / ML System

### Active Components
- Embeddings: SentenceTransformer `all-MiniLM-L6-v2`
- Retrieval: ChromaDB similarity search
- Response generation:
  - Primary: OpenAI chat model via LangChain (if key configured)
  - Fallback: deterministic template response (if key absent)
- Symptom analysis:
  - Extracted using heuristic keyword + regex
  - Structured triage generated by LLM or fallback rule set

### Interaction Flow

```text
User question
 -> symptom extraction (heuristics)
 -> query embedding generation
 -> Chroma search (top-k docs)
 -> assemble context + triage hints
 -> LLM prompt chain (or fallback)
 -> structured API response
```

### Voice AI Status
- Voice pathways are described in docs, but no active backend voice route/service implementation is present in current runtime code.

---

## 7. Data Pipeline

### YAML Datasets
- 10 YAML files in `data/` with healthcare-style conversational pairs
- Topics include greeting, fever, cough/cold, fracture, doctor requests, and personal/profile exchanges

### Ingestion Pipeline Components
- Loader and preprocessing utils: `backend/utils/text_processing.py`
- Medical chunking pipeline: `backend/rag/data_ingestion.py`
- Script entrypoint: `scripts/ingest_data.py`

### Actual Ingestion Flow

```text
data/*.yml
 -> load_yaml_files()
 -> process_medical_content()
 -> VectorDatabase.add_documents()
 -> Chroma persistent collection
```

### Important Gap
- `scripts/ingest_data.py` computes backend path as `scripts/backend` (non-existent), indicating path resolution bug for direct script execution.

### Vector Storage
- Persisted under `embeddings/chroma.sqlite3`
- Additional collection UUID folder currently present but empty

---

## 8. API Endpoints

Base backend app: `http://localhost:8000`
Primary prefix: `/api/v1`

### `GET /`
- Purpose: basic root metadata
- Response: `{ "message": "AI Healthcare Assistant API", "version": "1.0.0" }`

### `POST /api/v1/chat`
- Purpose: main RAG + symptom aware conversation endpoint
- Request body (`ChatRequest`):
  - `message: string` (required)
  - `conversation_id?: string`
  - `user_id?: string`
  - `symptoms?: string[]`
- Response (`ChatResponse`):
  - `response: string`
  - `conversation_id: string`
  - `sources?: string[]`
  - `symptom_analysis?: { symptoms, severity_score, risk_level, possible_conditions, urgency_recommendation }`
  - `disclaimer: string`

### `POST /api/v1/analyze-symptoms`
- Purpose: symptom-first analysis route
- Same request model, with validation for symptom/message presence
- Returns `ChatResponse`

### `GET /api/v1/health`
- Purpose: liveness + feature indication
- Response includes status/timestamp/version/features

### Frontend API Pathing
- Client calls `/api/v1/chat` on Next.js app
- Rewrite forwards to backend `/api/v1/chat`

---

## 9. Configuration & Environment Variables

### Config Files
- `backend/config/settings.py`
  - `openai_api_key` (currently optional default `""`)
  - `openai_model` default `gpt-3.5-turbo`
  - Chroma persistence + collection
  - app name/debug
  - allowed CORS origins
  - `.env` path expected at `backend/.env`
- `frontend/next.config.js`
  - dev rewrite proxy to backend
- `frontend/tailwind.config.js`, `postcss.config.js`, `tsconfig.json`

### Environment Variables Referenced (Code + Docs)
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (indirect via settings openai_model)
- `ELEVENLABS_API_KEY` (docs only in current repo state)
- `ELEVENLABS_VOICE_ID` (docs only)
- `ELEVENLABS_MODEL_ID` (docs only)
- `HOST`, `PORT`, `CORS_ORIGINS` (docs mention)

### Config Observations
- Docs still assume OpenAI key required at all times, but runtime now supports fallback mode.
- Voice-related env vars are documented but not actively consumed by runtime code.

---

## 10. Dependencies

### Major Python Dependencies
- `fastapi`, `uvicorn`: API server
- `pydantic`, `pydantic-settings`: schemas + env config
- `langchain`, `langchain-openai`: prompt and model orchestration
- `chromadb`: vector storage and retrieval
- `sentence-transformers`: embedding generation
- `openai`: LLM integration
- `pyyaml`: YAML corpus processing
- `pandas`, `tqdm`, `httpx`: utility/support libs

### Major Frontend Dependencies
- `next`, `react`, `react-dom`: application runtime
- `typescript`: static typing
- `tailwindcss`, `postcss`, `autoprefixer`: styling pipeline
- `lucide-react`: icon system
- `eslint`, `eslint-config-next`: linting

### Dependency State Observations
- Root `requirements.txt` and `backend/requirements.txt` differ (e.g., `langchain-openai` and `openai` versions)
- Runtime install strategy uses `backend/requirements.txt`

---

## 11. Deployment Architecture

### Local Development (Implemented)
- `setup.sh`: creates `.venv`, installs backend deps, installs frontend deps
- `run_backend.sh`: starts uvicorn `backend.main:app` on `:8000`
- `run_frontend.sh`: starts Next dev server on `:3000`
- `start.sh`: launches both scripts in background with trap cleanup

### Production References (Documented, Not in Active Tree)
- Docs mention Docker Compose, NGINX, CI/CD and Heroku patterns
- No active `docker/`, `docker-compose.yml`, or CI pipeline files in current repository snapshot

### Current Practical Deployment Reality
- Dev-script based local execution only
- No explicit container orchestration definitions present

---

## 12. Current Strengths

- Clear backend layering: API -> service -> retrieval/LLM
- Typed request/response models and enum-based risk levels
- Practical RAG baseline with persisted vector DB
- Good starter docs set (setup, architecture, roadmap, contributing)
- Modern, responsive frontend UX with dark mode and disclaimers
- Local startup scripts reduce setup friction
- Backend now resilient to missing OpenAI key for dev/testing

---

## 13. Architectural Problems

### 1) Duplicate / Legacy Systems
- Multiple architectural eras coexist:
  - Current FastAPI + Next.js RAG runtime
  - Legacy Flask/ChatterBot/voice references in docs and VS Code launch
- Unused frontend components/hooks remain in active tree.

### 2) Documentation Drift
- README/docs claim files/routes/features that do not exist in runtime (e.g., `frontend/app/api/chat/route.ts`, voice backend files).
- Setup docs reference old paths (`ai-healthcare-assistant` subtree) absent in repo.

### 3) Tight Coupling / Global Singleton
- `get_rag_service()` holds module-global singleton, limiting testability and multi-tenant patterns.

### 4) Reliability Risks
- Broad exception handling with generic 500 responses.
- Ingestion script backend path bug likely breaks standalone ingestion.
- ID generation in vector add uses per-call `doc_i`, risking collisions across repeated adds.

### 5) Security / Compliance Gaps
- No auth/authz, no rate limiting, no structured audit logs.
- No explicit prompt-injection mitigation layer.
- Healthcare disclaimers exist but no policy enforcement middleware.

### 6) Scalability Gaps
- No async background workers for heavy embedding/model operations.
- No caching or request queueing.
- Chroma local persistence only; no HA/distributed vector strategy.

### 7) Testing Gaps
- Limited backend tests (mostly service-level happy paths)
- No API integration tests against FastAPI app
- No frontend unit/integration tests

### 8) Repository Hygiene
- Build artifacts committed (`frontend/.next/`), virtualenv and pycache visible in workspace.
- Mixed dependency manifests and stale launch config.

---

## 14. Enterprise Readiness Score

Scored from 1 to 10 based on current code and operational artifacts.

- Architecture: 6/10
  - Solid baseline layering, but mixed legacy + active systems reduce clarity.
- Scalability: 4/10
  - Single-process local assumptions, no cache/queue/workers.
- Security: 3/10
  - Missing auth, rate limiting, centralized security controls.
- AI Pipeline: 6/10
  - Working RAG core with triage structure, but simplistic symptom extraction and limited guardrails.
- DevOps: 3/10
  - Script-based local start only; no live CI/CD/container manifests in current tree.
- Documentation: 6/10
  - Comprehensive but materially out of sync with running code.

Overall enterprise readiness (weighted average): **4.7/10**.

---

## 15. Recommended Improvements

### High Priority
- Unify architecture and remove/relocate legacy artifacts.
- Fix documentation drift: align README/docs with real routes/files/features.
- Add secure runtime baseline: auth, rate limiting, request tracing, structured logs.
- Repair ingestion script pathing and add ingestion integration tests.
- Introduce API contract tests for `/api/v1/*` endpoints.

### Medium Priority
- Extract service/repository interfaces for DI and testability.
- Add Redis cache for retrieval/prompt responses and configurable TTL.
- Replace heuristic symptom extraction with model-assisted entity extraction.
- Add frontend test coverage (component + E2E smoke tests).
- Normalize dependency management (single source of truth for backend deps).

### Low Priority
- Add conversation persistence/history model.
- Add multilingual support and accessibility improvements.
- Add admin analytics dashboard.
- Move to stricter TypeScript settings and shared UI primitives.

---

## 16. Suggested Enterprise Architecture

### Target Architecture (Proposed)

```text
[Web / Mobile Clients]
        |
[API Gateway / BFF]
        |
+-------------------------------+
| FastAPI App                   |
| - Auth Middleware             |
| - Rate Limit / WAF Hooks      |
| - Request Validation          |
+-------------------------------+
        |
+-------------------------------+
| Application Services          |
| - Chat Orchestrator           |
| - Symptom Triage Service      |
| - Citation/Source Service     |
| - Conversation Service        |
+-------------------------------+
        |
+-------------------------------+
| AI Layer                      |
| - Prompt Guardrails           |
| - LLM Provider Adapter        |
| - Embedding Service           |
+-------------------------------+
        |
+-------------------------------+
| Data Layer                    |
| - Vector Store (Chroma/PGV)   |
| - Relational DB (Postgres)    |
| - Cache (Redis)               |
+-------------------------------+
        |
+-------------------------------+
| Async Processing              |
| - Task Queue (Celery/RQ)      |
| - Ingestion/Batch Pipelines   |
+-------------------------------+
```

### Key Design Changes
- Separate router, service, repository, and AI-adapter interfaces.
- Add policy engine for medical safety and content filtering.
- Implement full observability (structured logs, metrics, tracing).
- Externalize all secrets/config and enforce environment profiles.
- Add CI/CD with lint/test/build/security scans and deployment gates.

### Migration Plan (Incremental)
1. Stabilize current monolith: cleanup + tests + docs sync.
2. Introduce DI interfaces and service boundaries.
3. Add auth/logging/rate limiting and persistent conversation storage.
4. Introduce async ingestion and caching.
5. Containerize + deploy with monitored staging/production environments.

---

## Appendix A: File-by-File Coverage Notes

All repository files in the active project tree were reviewed, including:
- Root scripts/config: `README.md`, `setup.sh`, `start.sh`, `run_backend.sh`, `run_frontend.sh`, `requirements.txt`, `.gitignore`
- Backend: all files under `backend/` listed in section 3
- Frontend: all source/config files under `frontend/` listed in section 3
- Data corpus: all 10 YAML files under `data/`
- Tests/scripts: `tests/test_backend.py`, `scripts/ingest_data.py`
- Governance/docs: all files under `docs/`, `.github/`, `.vscode/`
- Runtime artifacts observed: `embeddings/chroma.sqlite3`, `.next/` build outputs, `package-lock.json`

Excluded from deep architectural interpretation:
- `.git/*`, `.venv/*`, and generated binary/build internals (treated as tooling/runtime artifacts rather than source architecture).

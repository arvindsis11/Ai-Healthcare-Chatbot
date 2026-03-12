# GitHub Issues — AI Healthcare Platform

This document lists all proposed GitHub Issues for the **AI Healthcare Platform** repository.
Each issue is ready to be filed directly in GitHub using the issue templates provided in
`.github/ISSUE_TEMPLATE/`.

Issues are grouped by area and ordered roughly by priority.

---

## Table of Contents

1. [Feature Issues](#feature-issues)
2. [Bug / Reliability Issues](#bug--reliability-issues)
3. [Documentation Issues](#documentation-issues)
4. [Good First Issues](#good-first-issues)

---

## Feature Issues

---

### Issue 1

**Title:** Feature: Implement Real Translation API Integration

**Labels:** `enhancement`, `help wanted`

**Description:**
The `TranslationService` (`backend/app/ai/translation_service.py`) currently provides stub
implementations for `translate_to_english` and `translate_from_english` — both methods return
the original text unchanged. The language detection relies on a tiny hardcoded keyword list
(e.g., `"hola"`, `"bukhar"`). This means the advertised multilingual support (Hindi, Spanish,
French) does not actually work for non-English users.

Replacing the stubs with a real translation backend will make the multilingual feature
genuinely usable and improve accessibility for non-English-speaking patients worldwide.

**Proposed Solution:**
Integrate a production-grade translation API as a pluggable backend:
- Option A (open-source, no cost): `Helsinki-NLP` MarianMT models via `transformers`.
- Option B (accuracy-first): Google Cloud Translation API or DeepL API with API-key configuration.
- Improve language detection with the `langdetect` or `lingua` library instead of keyword matching.

**Tasks:**
- [ ] Replace keyword-based `detect_language()` with `langdetect` or `lingua` library call.
- [ ] Implement `translate_to_english()` using MarianMT or a configurable external API.
- [ ] Implement `translate_from_english()` with the same backend.
- [ ] Add `TRANSLATION_API_KEY` and `TRANSLATION_PROVIDER` to `Settings` and `.env.example`.
- [ ] Unit-test detection accuracy for all four supported languages.
- [ ] Update `docs/AI_MODEL.md` to document the translation integration.

---

### Issue 2

**Title:** Feature: Add PostgreSQL-Backed Session Persistence

**Labels:** `enhancement`, `help wanted`

**Description:**
`SessionRepository` (`backend/app/repositories/session_repository.py`) is an in-memory store.
All conversation history is lost every time the server restarts. The repository README and
`backend/app/repositories/sql/postgres_schema.sql` already have a PostgreSQL schema defined,
but the actual PostgreSQL-backed implementation is missing.

Without durable persistence, users lose their entire conversation history on every deployment,
making the "conversation history" feature unreliable in production.

**Proposed Solution:**
Implement a `PostgresSessionRepository` that satisfies the same interface as the existing
`SessionRepository` and is selected via the `DATABASE_URL` setting:
- Use `psycopg` (already in `requirements.txt`) for async queries.
- Fall back to the in-memory repository when `DATABASE_URL` is empty.
- Expose a `GET /api/v1/sessions/{conversation_id}` endpoint (already implemented in the router)
  backed by the new repository.

**Tasks:**
- [ ] Implement `PostgresSessionRepository` with `append_message` and `get_messages` methods.
- [ ] Apply the existing `postgres_schema.sql` schema via a migration script or Alembic.
- [ ] Update `get_session_repository()` dependency factory to select between in-memory and Postgres.
- [ ] Add `DATABASE_URL` to `.env.example` with a sample connection string.
- [ ] Write integration tests using a Docker-based PostgreSQL fixture.
- [ ] Update `docs/DEPLOYMENT.md` to document PostgreSQL setup.

---

### Issue 3

**Title:** Feature: Implement JWT / OAuth2 Authentication

**Labels:** `enhancement`, `help wanted`

**Description:**
The API currently has no authentication layer. Every endpoint is publicly accessible without
any identity verification. This is a critical gap for Phase 2 of the product roadmap
("Multi-tenant API Management"). Without authentication, there is no way to:
- Protect user session data.
- Issue per-user conversation histories.
- Enforce per-tenant rate limits.
- Build any billing or access-control features.

**Proposed Solution:**
Add an OAuth2 password-bearer JWT flow using `python-jose` and `passlib`:
- `POST /api/v1/auth/token` — issue JWT on valid credentials.
- `GET /api/v1/auth/me` — return current user profile.
- Protect chat/session endpoints with a `get_current_user` FastAPI dependency.
- Store users in PostgreSQL (extends the session schema).

**Tasks:**
- [ ] Add `python-jose[cryptography]` and `passlib[bcrypt]` to `backend/requirements.txt`.
- [ ] Create `backend/app/models/user.py` with `User` and `Token` Pydantic schemas.
- [ ] Implement `UserRepository` backed by PostgreSQL.
- [ ] Create `backend/app/api/auth.py` router with `/token` and `/me` endpoints.
- [ ] Add `get_current_user` dependency and apply it to `/chat`, `/sessions`, and `/analyze-symptoms`.
- [ ] Add `SECRET_KEY` and `ACCESS_TOKEN_EXPIRE_MINUTES` to `Settings` and `.env.example`.
- [ ] Write unit and integration tests for auth endpoints.
- [ ] Document the auth flow in `docs/API.md`.

---

### Issue 4

**Title:** Feature: Add Whisper Speech-to-Text Voice Input

**Labels:** `enhancement`, `help wanted`

**Description:**
The README and `docs/AI_MODEL.md` list **Whisper** as a supported AI model, but there is no
speech-to-text implementation anywhere in the codebase. Users cannot interact with the chatbot
via voice, which is important for accessibility and mobile-first use cases.

**Proposed Solution:**
- Backend: Add `POST /api/v1/transcribe` that accepts an audio file upload (WAV/MP3/OGG) and
  returns a transcript using `openai-whisper` (local) or the OpenAI Transcription API.
- Frontend: Add a microphone button to `InputBar.tsx` that records audio via the browser
  `MediaRecorder` API, sends it to `/api/v1/transcribe`, and populates the chat input.

**Tasks:**
- [ ] Add `openai` audio transcription call (or `openai-whisper` local model) to a new
  `backend/app/services/transcription_service.py`.
- [ ] Create `POST /api/v1/transcribe` endpoint accepting `multipart/form-data`.
- [ ] Add `WHISPER_MODEL` setting (`"whisper-1"` for API, or `"base"` for local).
- [ ] Add microphone icon button to `InputBar.tsx` with recording state.
- [ ] Stream audio blob to transcription endpoint and inject result into chat input.
- [ ] Write tests for the transcription endpoint with a mock audio file.
- [ ] Update `docs/AI_MODEL.md` with Whisper setup instructions.

---

### Issue 5

**Title:** Feature: Add ElevenLabs Text-to-Speech Voice Output

**Labels:** `enhancement`, `help wanted`

**Description:**
`docs/AI_MODEL.md` lists **ElevenLabs** for text-to-speech, but there is no implementation
in the codebase. Adding voice output improves accessibility (especially for visually impaired
users) and makes the interaction feel more natural.

**Proposed Solution:**
- Backend: Add `POST /api/v1/speak` that accepts a text payload and returns an audio stream
  using the ElevenLabs Python SDK.
- Frontend: Add a speaker icon to `MessageBubble.tsx` on assistant messages that triggers
  audio playback.

**Tasks:**
- [ ] Add `elevenlabs` to `backend/requirements.txt`.
- [ ] Create `backend/app/services/tts_service.py` with an `ElevenLabsTTSService` class.
- [ ] Implement `POST /api/v1/speak` that returns `audio/mpeg` stream.
- [ ] Add `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` to `Settings` and `.env.example`.
- [ ] Add speaker icon button to `MessageBubble.tsx`; play response audio on click.
- [ ] Write tests mocking the ElevenLabs SDK response.
- [ ] Update `docs/AI_MODEL.md` with ElevenLabs setup instructions.

---

### Issue 6

**Title:** Feature: Implement Real-Time Streaming Chat Responses (SSE)

**Labels:** `enhancement`, `help wanted`

**Description:**
The `/api/v1/chat` endpoint returns the full LLM response in a single blocking HTTP call.
For long-form medical answers this can take several seconds, leaving the user staring at
"Generating response…" with no feedback. Streaming via Server-Sent Events (SSE) or
chunked responses would improve the perceived performance significantly.

**Proposed Solution:**
- Use LangChain's `astream` API with FastAPI's `StreamingResponse` to emit tokens as they
  are generated.
- Frontend: Replace the single `fetch` call in `chatService.ts` with an `EventSource` or
  `ReadableStream` reader that appends tokens to the last assistant message in real time.

**Tasks:**
- [ ] Add `stream: bool = False` field to `ChatRequest`.
- [ ] Implement an async generator in `LLMService.stream_medical_response()` using `astream`.
- [ ] Return `StreamingResponse(media_type="text/event-stream")` from the chat endpoint when
  `stream=True`.
- [ ] Update `chatService.ts` to support streaming via `ReadableStream` when requested.
- [ ] Update `ChatWorkspace.tsx` to append streamed tokens to the assistant message in state.
- [ ] Add integration tests asserting correct SSE event format.
- [ ] Document the streaming API in `docs/API.md`.

---

### Issue 7

**Title:** Feature: Connect Admin Dashboard to Real Backend Metrics

**Labels:** `enhancement`, `help wanted`

**Description:**
The Admin Dashboard (`frontend/src/app/admin/page.tsx`) displays hardcoded placeholder
values (e.g., "12,480 daily active users", "143ms avg latency"). These are completely fake
and provide no operational insight. A real analytics backend is needed to make the dashboard
useful for monitoring the chatbot in production.

**Proposed Solution:**
- Backend: Add `GET /api/v1/admin/metrics` endpoint that returns aggregated stats:
  - Total conversations today / 7 days.
  - Average request latency (tracked in structured logs or Redis counters).
  - High-risk alert count.
  - Top-10 symptom terms from recent queries.
- Frontend: Replace hardcoded values with a `useEffect` call to the metrics endpoint.

**Tasks:**
- [ ] Create `backend/app/services/analytics_service.py` with in-memory counters (upgradeable
  to Redis/PostgreSQL).
- [ ] Increment counters in the chat endpoint middleware on each request.
- [ ] Add `GET /api/v1/admin/metrics` endpoint returning real data.
- [ ] Create `frontend/src/services/adminService.ts` to fetch metrics.
- [ ] Refactor `MetricsCards.tsx` to accept dynamic data from the service.
- [ ] Add a `useEffect` data-fetch in `AdminDashboardPage` with a loading/error state.
- [ ] Write tests for the metrics endpoint.

---

### Issue 8

**Title:** Feature: Expand Symptom Extraction with Medical NER (spaCy)

**Labels:** `enhancement`, `help wanted`

**Description:**
`SymptomExtractionService` (`backend/app/services/medical_intelligence_service.py`) uses a
hardcoded list of nine symptom keywords. This misses the vast majority of symptoms users
describe in free text. The `spaCy` library is already a dependency and partially wired in,
but the model (`en_core_web_sm`) is a general-purpose model, not a medical NER model.

Improving symptom extraction accuracy directly improves triage quality and doctor
recommendations.

**Proposed Solution:**
- Integrate `scispacy` with the `en_ner_bc5cdr_md` model (diseases and chemicals) or
  `en_core_med7_lg` for full medical NER.
- Fall back to the existing keyword list when the model is unavailable.
- Expand the keyword list to include at least the top-100 common symptoms as a fast path.

**Tasks:**
- [ ] Add `scispacy` and the chosen medical model to `backend/requirements.txt`.
- [ ] Update `SymptomExtractionService.__post_init__` to try loading the medical NER model.
- [ ] Implement NER-based extraction alongside the keyword extraction.
- [ ] Expand the keyword fallback list from 9 to 100+ common symptoms.
- [ ] Write unit tests comparing extraction results on a set of sample symptom descriptions.
- [ ] Benchmark extraction latency and document it in `docs/AI_MODEL.md`.

---

### Issue 9

**Title:** Feature: Expand RAG Knowledge Base with Medical PDFs and FHIR Data

**Labels:** `enhancement`, `help wanted`

**Description:**
The current knowledge base (`data/` directory) consists of simple YAML chat files for a
handful of conditions (fever, cough, headache, fracture). This gives ChromaDB very little
medical content to retrieve from, leading to low-quality citations and context for the LLM.

Ingesting authoritative medical documents (WHO guidelines, CDC fact sheets, or open FHIR
resources) would dramatically improve response quality.

**Proposed Solution:**
- Add a `scripts/ingest_pdfs.py` script that reads PDF files from a configurable directory
  using `pypdf` or `pdfplumber`, chunks them, and ingests them into ChromaDB.
- Add a curated set of open-license medical PDFs as seed data (e.g., WHO symptom fact sheets).
- Update `scripts/ingest_data.py` to also ingest the new PDF corpus.

**Tasks:**
- [ ] Add `pypdf` or `pdfplumber` to `backend/requirements.txt`.
- [ ] Create `scripts/ingest_pdfs.py` with configurable input directory and chunk size.
- [ ] Add at least 10 WHO/CDC open-license health fact sheets as PDF seed data.
- [ ] Update `docker-compose.yml` to run ingestion on first startup if collection is empty.
- [ ] Add `KNOWLEDGE_BASE_DIR` setting to `Settings` and `.env.example`.
- [ ] Write tests that assert document count increases after ingestion.
- [ ] Document the ingestion process in `docs/RAG_PIPELINE.md`.

---

### Issue 10

**Title:** Feature: Add Appointment Scheduling Scaffold (Phase 3 Roadmap)

**Labels:** `enhancement`, `help wanted`

**Description:**
Phase 3 of the product roadmap includes doctor-network integration and appointment scheduling.
Adding a basic appointment scheduling scaffold now will allow community contributors to build
on top of it incrementally without needing to design the data model from scratch.

**Proposed Solution:**
- Add a minimal `Appointment` Pydantic model and `AppointmentRepository` (in-memory, upgradeable
  to PostgreSQL).
- Add `POST /api/v1/appointments` and `GET /api/v1/appointments/{appointment_id}` endpoints.
- Surface a "Book Appointment" button in `SymptomAnalysisPanel.tsx` that links to a placeholder
  booking form.

**Tasks:**
- [ ] Create `backend/app/models/appointment.py` with `Appointment`, `AppointmentRequest`, and
  `AppointmentStatus` schemas.
- [ ] Create `backend/app/repositories/appointment_repository.py` (in-memory scaffold).
- [ ] Create `backend/app/api/appointments.py` router with create and get endpoints.
- [ ] Register the new router in `backend/app/main.py`.
- [ ] Add a "Book Appointment" button to `SymptomAnalysisPanel.tsx`.
- [ ] Write tests for the appointment endpoints.
- [ ] Add appointment schema to `postgres_schema.sql`.

---

## Bug / Reliability Issues

---

### Issue 11

**Title:** Bug: Prompt Injection Guard Has Insufficient Pattern Coverage

**Labels:** `bug`, `enhancement`

**Description:**
`is_prompt_injection()` in `backend/app/ai/prompt_guard.py` checks for only five hardcoded
patterns. A determined user can trivially bypass these checks with slight variations
(e.g., `"Ignore all previous instructions"`, `"disregard the system prompt"`,
`"act as DAN"`, `"you are now in developer mode"`).

In a medical chatbot, successful prompt injection could cause the LLM to provide dangerous
misinformation or bypass medical safety guardrails — a serious safety and liability risk.

**Proposed Solution:**
- Expand the pattern list with common jailbreak and injection variants (case-insensitive,
  partial-match).
- Add a configurable blocklist file so patterns can be updated without code changes.
- Consider a lightweight ML-based injection classifier as a secondary layer.

**Tasks:**
- [ ] Audit current patterns against known jailbreak databases (e.g., jailbreakchat.com patterns).
- [ ] Expand `SUSPICIOUS_PATTERNS` to cover at least 30 common injection phrases and variants.
- [ ] Add normalisation (strip extra whitespace, leetspeak substitutions) before matching.
- [ ] Load additional patterns from an optional `PROMPT_GUARD_BLOCKLIST` file path in settings.
- [ ] Write parameterised tests covering all new patterns and known bypasses.
- [ ] Document the threat model in `docs/SECURITY.md`.

---

### Issue 12

**Title:** Bug: In-Memory SessionRepository Loses All Conversation History on Restart

**Labels:** `bug`

**Description:**
`SessionRepository` uses a plain Python dictionary as storage. Any server restart, container
redeploy, or horizontal scale-out causes all conversation history to be silently lost.
The `GET /api/v1/sessions/{conversation_id}` endpoint will return an empty message list
after restart, and the frontend chat history sidebar will appear empty — with no user
notification.

**Proposed Solution:**
This is the in-memory scaffolding intended to be replaced. The fix is to implement
`PostgresSessionRepository` (see Issue 2). As a minimal short-term fix:
- Return a clear error or warning in the API response when the session was not found,
  rather than silently returning an empty list.
- Document the limitation in `docs/PROJECT_STATE.md`.

**Tasks:**
- [ ] Add a `session_not_found` flag to the `GET /api/v1/sessions` response when the ID
  does not exist.
- [ ] Update the frontend to display "Session not found — conversation history may have been
  reset" when the flag is set.
- [ ] Add a note to `docs/PROJECT_STATE.md` documenting the current in-memory limitation.
- [ ] Implement `PostgresSessionRepository` as the durable solution (see Issue 2).

---

### Issue 13

**Title:** Bug: DoctorRecommendationService Logic Is Overly Simplistic

**Labels:** `bug`, `enhancement`

**Description:**
`DoctorRecommendationService.recommend()` in `medical_intelligence_service.py` returns a
specialist based on a few substring checks against a joined symptom string. This causes
several problems:
- `"children"` as a symptom triggers a Pediatrician recommendation (no patient contains
  "children" as a symptom — the intent was pediatric patients).
- Only five specialties are covered; common cases like gastrointestinal, respiratory,
  and orthopaedic conditions are all funnelled to "General Physician".
- There is no confidence score or rationale returned.

**Proposed Solution:**
- Replace string matching with a symptom-to-specialty mapping table covering the top-20
  symptom clusters mapped to their primary specialties.
- Remove the nonsensical `"children"` check.
- Return both a primary and an alternative specialist recommendation.

**Tasks:**
- [ ] Design a symptom-to-specialty mapping covering at least 20 symptom clusters.
- [ ] Rewrite `recommend()` to use the mapping and return a ranked list of specialists.
- [ ] Remove the `"children"` substring check.
- [ ] Add `alternative_specialist` field to `ChatResponse`.
- [ ] Update the frontend `SymptomAnalysisPanel.tsx` to display the alternative specialist.
- [ ] Write unit tests covering the new mapping logic.

---

### Issue 14

**Title:** Bug: Missing `.env.example` Configuration File

**Labels:** `bug`, `documentation`, `good first issue`

**Description:**
There is no `.env.example` file in the repository. New contributors who clone the project
have no reference for which environment variables are required. The `Settings` class in
`backend/app/core/settings.py` defines the full list of variables, but developers must read
the source code to discover them. This increases onboarding friction and frequently causes
`ValidationError` failures on first run.

**Proposed Solution:**
Create a `.env.example` file at the repository root listing every variable from `Settings`
with placeholder or default values and inline comments.

**Tasks:**
- [ ] Create `.env.example` at the repository root.
- [ ] Include all variables from `backend/app/core/settings.py` with comments.
- [ ] Add a note about which variables are required vs optional.
- [ ] Reference `.env.example` in `README.md` Quick Start section.
- [ ] Add `.env` to `.gitignore` if not already present (it already is — just verify).

---

## Documentation Issues

---

### Issue 15

**Title:** Docs: Add API Reference with Request/Response Examples

**Labels:** `documentation`, `good first issue`

**Description:**
`docs/API.md` exists but provides only endpoint names without request/response schemas,
example `curl` commands, or error code documentation. Contributors building integrations or
writing tests must read the source code to understand the API contract.

**Proposed Solution:**
Expand `docs/API.md` with full OpenAPI-style documentation for every endpoint, including:
- Request body schema (with types and required/optional fields).
- Response body schema.
- Example `curl` request and JSON response.
- Error codes and their meaning.

**Tasks:**
- [ ] Document `POST /api/v1/chat` — request, response, error codes.
- [ ] Document `POST /api/v1/analyze-symptoms`.
- [ ] Document `GET /api/v1/health`.
- [ ] Document `GET /api/v1/sessions/{conversation_id}`.
- [ ] Add a global error-code table (400, 413, 429, 500).
- [ ] Add example `curl` command for each endpoint.
- [ ] Cross-link to `http://localhost:8000/docs` (Swagger UI) in the README.

---

### Issue 16

**Title:** Docs: Add CODE_OF_CONDUCT.md

**Labels:** `documentation`, `good first issue`

**Description:**
The repository has no `CODE_OF_CONDUCT.md`. A code of conduct is a standard expectation for
open-source projects and is required for GitHub's "Community Standards" checklist. Without it,
contributors lack clear guidance on acceptable behavior and there is no documented process for
handling misconduct.

**Proposed Solution:**
Add a `CODE_OF_CONDUCT.md` at the repository root based on the
[Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

**Tasks:**
- [ ] Create `CODE_OF_CONDUCT.md` at the repository root.
- [ ] Use the Contributor Covenant v2.1 as the base template.
- [ ] Add project-specific contact information for reporting violations.
- [ ] Link to `CODE_OF_CONDUCT.md` from `README.md` and `docs/CONTRIBUTING.md`.

---

### Issue 17

**Title:** Docs: Document the RAG Pipeline with Data Flow Diagrams

**Labels:** `documentation`

**Description:**
`docs/RAG_PIPELINE.md` exists but describes the pipeline at a very high level. Contributors
who want to improve the retrieval or re-ranking logic need to understand the exact data flow:
how queries are embedded, how `n_results=8` documents are fetched, how the keyword reranker
works, and how context is chunked before the LLM prompt is built.

**Proposed Solution:**
Expand `docs/RAG_PIPELINE.md` with:
- A Mermaid sequence diagram of a single chat request end-to-end.
- Annotated code references for each pipeline step.
- Configuration knobs (chunk size, top-k, reranking weights) and how to tune them.

**Tasks:**
- [ ] Add a Mermaid sequence diagram covering: query → embed → vector search → rerank → chunk
  → LLM prompt → response.
- [ ] Document `n_results`, `max_words` chunk size, and reranking formula with tuning guidance.
- [ ] Explain the `_keyword_overlap_score` reranking heuristic and its trade-offs.
- [ ] Add a section on how to extend the knowledge base (link to ingestion scripts).
- [ ] Cross-link from `README.md` Architecture section.

---

### Issue 18

**Title:** Docs: Improve CONTRIBUTING.md with Development Environment Details

**Labels:** `documentation`, `good first issue`

**Description:**
`docs/CONTRIBUTING.md` is minimal. It covers the PR flow but omits:
- How to set up the Python virtual environment.
- How to install spaCy models (`python -m spacy download en_core_web_sm`).
- How to run tests (`pytest tests/`).
- How to run the linter (`ruff check backend`).
- How to populate ChromaDB for local development.

New contributors regularly encounter failures that a richer CONTRIBUTING.md would prevent.

**Proposed Solution:**
Expand `docs/CONTRIBUTING.md` with a full "Development Environment" section covering every
manual step from clone to running tests.

**Tasks:**
- [ ] Add a "Prerequisites" section listing Python 3.11+, Node 20+, Docker.
- [ ] Add a "Backend Setup" section with venv creation, pip install, spaCy model download.
- [ ] Add a "Frontend Setup" section with `npm install`.
- [ ] Add a "Running Tests" section with `pytest` and frontend `jest` commands.
- [ ] Add a "Linting" section with `ruff` and `eslint` commands.
- [ ] Add a "Seeding the Knowledge Base" section referencing `scripts/ingest_data.py`.

---

## Good First Issues

---

### Issue 19

**Title:** Good First Issue: Add `.env.example` Configuration File

**Labels:** `good first issue`, `documentation`

**Description:**
See Issue 14 above. This is a great first contribution because it requires only reading the
`Settings` class and creating a new file — no complex code changes needed.

**Proposed Solution:**
Create `.env.example` at the repository root with all environment variables from
`backend/app/core/settings.py`.

**Tasks:**
- [ ] Read `backend/app/core/settings.py` and list all settings variables.
- [ ] Create `.env.example` with placeholder values and inline comments.
- [ ] Reference the file in the `README.md` Quick Start section.

---

### Issue 20

**Title:** Good First Issue: Add Keyboard Shortcut (Ctrl+Enter) to Submit Chat Message

**Labels:** `good first issue`, `enhancement`

**Description:**
The chat input (`frontend/src/components/InputBar.tsx`) only submits when the Send button is
clicked. Adding a `Ctrl+Enter` (or `Cmd+Enter` on macOS) keyboard shortcut is a common UX
pattern in chat interfaces and reduces friction for power users.

**Proposed Solution:**
Add a `onKeyDown` handler to the `<textarea>` in `InputBar.tsx` that calls `onSend` when
`Ctrl+Enter` or `Cmd+Enter` is detected.

**Tasks:**
- [ ] Open `frontend/src/components/InputBar.tsx`.
- [ ] Add a `handleKeyDown` function that detects `(e.ctrlKey || e.metaKey) && e.key === 'Enter'`.
- [ ] Call `onSend(text)` and clear the input on that keypress.
- [ ] Update the input placeholder to hint at the shortcut: `"Type a message… (Ctrl+Enter to send)"`.
- [ ] Write a Jest test asserting `onSend` is called on `Ctrl+Enter`.

---

### Issue 21

**Title:** Good First Issue: Add Loading Skeleton to Message List

**Labels:** `good first issue`, `enhancement`

**Description:**
When the API is processing a chat request, `ChatWorkspace.tsx` shows only the text
`"Generating response…"`. A skeleton loading animation would look more polished and give
users a clear visual indication that the request is in flight.

**Proposed Solution:**
Create a `MessageSkeleton` component that renders an animated shimmer placeholder and renders
it instead of the plain text while `isLoading` is true.

**Tasks:**
- [ ] Create `frontend/src/components/MessageSkeleton.tsx` with a Tailwind CSS shimmer animation.
- [ ] Replace the `"Generating response…"` paragraph in `ChatWorkspace.tsx` with `<MessageSkeleton />`.
- [ ] Write a Jest snapshot test for `MessageSkeleton`.

---

### Issue 22

**Title:** Good First Issue: Display Medical Disclaimer on First Load

**Labels:** `good first issue`, `enhancement`

**Description:**
The medical disclaimer banner in `ChatWorkspace.tsx` is always visible at the top but easy
to miss. Many healthcare chat applications show a modal disclaimer on first visit that
requires explicit acknowledgement. This helps manage liability and ensures users understand
the tool's limitations before they interact with it.

**Proposed Solution:**
Add a one-time modal dialog that appears on first page load (using `localStorage` to avoid
showing it on every visit) asking the user to acknowledge the medical disclaimer.

**Tasks:**
- [ ] Create `frontend/src/components/DisclaimerModal.tsx` with "I Understand" button.
- [ ] Use `localStorage.getItem('disclaimer_accepted')` to gate the modal display.
- [ ] Set `localStorage.setItem('disclaimer_accepted', 'true')` on acknowledgement.
- [ ] Import and render `<DisclaimerModal />` in `ChatWorkspace.tsx`.
- [ ] Write a Jest test asserting the modal is hidden after acknowledgement.

---

### Issue 23

**Title:** Good First Issue: Add Frontend Test Coverage for ChatService

**Labels:** `good first issue`, `documentation`

**Description:**
`frontend/src/services/chatService.ts` has no tests. It contains all HTTP communication logic
between the frontend and the backend API. Adding tests for this service with mocked `fetch`
calls will catch regressions when the API contract changes.

**Proposed Solution:**
Create `frontend/src/services/chatService.test.ts` with Jest tests for `sendChatMessage` and
`fetchSessionHistory`, using `jest.spyOn(global, 'fetch')` to mock responses.

**Tasks:**
- [ ] Create `frontend/src/services/chatService.test.ts`.
- [ ] Mock `fetch` to return a valid `ChatApiResponse` and assert the promise resolves correctly.
- [ ] Mock `fetch` to return a non-OK status and assert the promise rejects.
- [ ] Write a test for `fetchSessionHistory` with a mocked session response.
- [ ] Run `npm test` to ensure all tests pass.

---

### Issue 24

**Title:** Good First Issue: Add Ruff Pre-commit Hook for Backend Linting

**Labels:** `good first issue`, `enhancement`

**Description:**
The backend CI pipeline runs `ruff check backend`, but there is no pre-commit hook to
enforce linting locally before developers push. This means lint failures are only caught in
CI, slowing down the feedback loop.

**Proposed Solution:**
Add a `.pre-commit-config.yaml` at the repository root with `ruff` for Python and
`eslint` for TypeScript, and document setup in `docs/CONTRIBUTING.md`.

**Tasks:**
- [ ] Create `.pre-commit-config.yaml` with `ruff` hook targeting `backend/`.
- [ ] Add `eslint` hook targeting `frontend/src/`.
- [ ] Add `pre-commit install` to `setup.sh`.
- [ ] Document the pre-commit setup in `docs/CONTRIBUTING.md`.
- [ ] Add `pre-commit` to the backend CI workflow so it runs in GitHub Actions too.

# Copilot Instructions — AI Healthcare Chatbot (Enterprise Development Guide)

This document defines **global coding rules, architecture standards, and AI development guidelines** for GitHub Copilot when generating code for this repository.

Copilot should always follow these rules when suggesting or generating code.

---

# 1. Project Overview

This repository contains an **AI Healthcare Chatbot with Retrieval-Augmented Generation (RAG)**.

The system provides conversational healthcare assistance using:

* FastAPI backend
* Next.js frontend
* LangChain LLM orchestration
* ChromaDB vector search
* Sentence Transformers embeddings
* OpenAI GPT models
* Whisper speech recognition
* ElevenLabs text-to-speech

The goal of this project is to evolve into an **enterprise-grade AI healthcare assistant platform**.

---

# 2. Core Development Principles

Copilot must follow these principles when generating code:

1. **Do not break existing functionality.**
2. **Refactor incrementally instead of rewriting working code.**
3. **Keep the application runnable after every change.**
4. **Follow modular and layered architecture.**
5. **Write production-ready code.**
6. **Avoid unnecessary dependencies.**
7. **Ensure scalability and maintainability.**
8. **Document complex logic clearly.**
9. **Prefer asynchronous implementations where appropriate.**
10. **Maintain strict separation between layers.**

---

# 3. System Architecture

The system follows a **layered architecture**.

```
Frontend (Next.js + React + TypeScript)
        │
        ▼
API Layer (FastAPI routes)
        │
        ▼
Service Layer (business logic)
        │
        ▼
RAG Layer (vector retrieval + embeddings)
        │
        ▼
Repository Layer (database + vector store)
```

---

# 4. Backend Architecture Rules

Backend code must follow this structure:

```
backend/
  app/
    api/           # FastAPI routes
    services/      # business logic
    repositories/  # database + vector access
    rag/           # RAG pipeline
    models/        # Pydantic schemas
    core/          # config, logging, security
    middleware/    # request middleware
```

### API Layer

* Contains only FastAPI routes
* Must not contain business logic
* Calls service layer

Example:

```python
@router.post("/chat")
async def chat(request: ChatRequest):
    return await chatbot_service.process_message(request)
```

---

### Service Layer

Contains business logic.

Examples:

* LLM interaction
* response generation
* symptom analysis
* orchestration between services

Services should be stateless where possible.

---

### Repository Layer

Responsible for:

* database access
* vector database queries
* external data sources

Examples:

* ChromaDB repository
* PostgreSQL repository

---

### RAG Layer

Responsible for:

* embedding generation
* semantic search
* document retrieval
* context assembly

Pipeline:

```
query
 → embedding
 → vector search
 → retrieve top documents
 → inject context into LLM prompt
```

---

# 5. Frontend Architecture Rules

Frontend uses **Next.js App Router**.

Structure:

```
frontend/
  src/
    components/
    hooks/
    services/
    store/
    types/
```

Guidelines:

* UI components should be reusable.
* API calls must be placed in the `services` layer.
* Global state should use Zustand or React Context.
* Avoid API calls directly inside UI components.

Example:

```
services/chatService.ts
```

---

# 6. RAG Development Guidelines

The RAG system must follow these principles:

1. Use semantic embeddings.
2. Retrieve top-k relevant documents.
3. Inject retrieved context into LLM prompts.
4. Provide source citations where possible.
5. Avoid hallucinated medical advice.

Pipeline:

```
User Query
 → embedding
 → ChromaDB similarity search
 → retrieve context
 → construct prompt
 → generate response
```

---

# 7. Medical Safety Rules

This project operates in the **healthcare domain**.

All generated responses must follow medical safety guidelines.

The chatbot must:

* Never provide medical diagnosis
* Always recommend consulting healthcare professionals
* Provide general health guidance only
* Include medical disclaimers

Example:

```
"This information is for general educational purposes only and is not a substitute for professional medical advice."
```

---

# 8. Prompt Engineering Rules

LLM prompts must include:

* safety guardrails
* clear instructions
* structured outputs where possible

Example structured output:

```
{
  severity_score: number,
  risk_level: "low | medium | high",
  possible_conditions: string[],
  urgency_recommendation: string
}
```

---

# 9. Performance Optimization Guidelines

Copilot should prefer:

* async APIs
* caching
* batch processing
* vector search optimization

Use Redis caching when appropriate.

Example cache key:

```
chat:{hash(user_query)}
```

---

# 10. Security Rules

The system must include:

* input validation
* request size limits
* prompt injection protection
* CORS configuration
* rate limiting

Never expose API keys in frontend code.

---

# 11. Logging & Observability

The backend must implement structured logging.

Log fields:

```
timestamp
service
endpoint
request_id
latency
error
```

Example log:

```
{
  "timestamp": "2026-03-11T10:00:00",
  "service": "healthcare-chatbot",
  "endpoint": "/api/chat",
  "duration_ms": 120
}
```

---

# 12. Testing Guidelines

Backend testing:

* pytest
* API tests
* service unit tests

Frontend testing:

* Jest
* React Testing Library

Test coverage target: **80%+**

---

# 13. DevOps Guidelines

Deployment stack:

```
Frontend → Next.js
Backend → FastAPI
Vector DB → ChromaDB
Cache → Redis
Database → PostgreSQL
Proxy → NGINX
```

Infrastructure must support:

* Docker
* docker-compose
* CI/CD pipelines
* scalable deployment

---

# 14. AI Model Usage Guidelines

Primary models:

| Model                 | Purpose             |
| --------------------- | ------------------- |
| GPT                   | response generation |
| Sentence Transformers | embeddings          |
| Whisper               | speech recognition  |
| ElevenLabs            | text-to-speech      |

Prefer:

* deterministic outputs
* lower temperature for medical responses

Recommended temperature:

```
temperature = 0.3
```

---

# 15. Code Quality Standards

Copilot should generate code that follows:

* PEP8 for Python
* ESLint rules for TypeScript
* descriptive variable names
* modular functions
* clear docstrings

Avoid:

* overly complex functions
* hardcoded values
* duplicate code

---

# 16. Documentation Rules

When generating new features, Copilot should:

* update README if necessary
* update architecture docs
* add comments explaining logic

---

# 17. Enterprise Feature Direction

Future development should support:

* authentication
* chat history persistence
* analytics dashboards
* doctor recommendation systems
* multilingual support
* healthcare knowledge expansion
* local LLM deployment

---

# 18. What Copilot Should Avoid

Copilot must avoid:

* breaking API contracts
* removing working functionality
* unsafe medical advice
* adding large dependencies unnecessarily
* introducing untested experimental frameworks

---

# 19. Key Goal

The long-term goal of this repository is to build a **scalable, enterprise-grade AI healthcare assistant platform** that demonstrates:

* modern AI architecture
* safe medical AI design
* high-quality open-source engineering
* production-ready deployment patterns

---

# End of Instructions
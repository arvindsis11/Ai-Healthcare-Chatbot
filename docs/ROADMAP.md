# Project Roadmap

## Current Baseline

- FastAPI backend under `backend/app`
- Next.js frontend under `frontend/src`
- RAG pipeline using ChromaDB + SentenceTransformers
- Symptom analysis and risk-level UI rendering

## High Priority

- Add authentication and authorization
- Add request rate limiting and structured logging
- Add API integration tests for `/api/v1/*`
- Add frontend component and E2E tests
- Add docs for deployment and observability

## Medium Priority

- Extract dependency injection interfaces for repositories/services
- Add Redis caching for repeated prompts/retrieval
- Improve symptom extraction with model-assisted entities
- Add conversation history persistence

## Low Priority

- Multilingual support
- Analytics dashboard
- Voice pipeline reintroduction behind explicit feature flag

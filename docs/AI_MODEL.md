# AI Model Documentation

This project currently uses a RAG pipeline with retrieval + LLM response generation.

## Active Model Components

- LLM orchestration: LangChain
- LLM provider: OpenAI Chat model (when `OPENAI_API_KEY` is configured)
- Fallback mode: deterministic safe response when no API key is configured
- Embeddings: SentenceTransformers (`all-MiniLM-L6-v2`)
- Vector DB: ChromaDB persistent store

## Symptom Analysis

- Initial symptom extraction is heuristic (keyword + regex) in `backend/app/services/rag_service.py`.
- Structured triage output is generated as:
  - `severity_score`
  - `risk_level`
  - `possible_conditions`
  - `urgency_recommendation`

## Prompt Safety

`backend/app/services/llm_service.py` enforces a medical safety-oriented system prompt:

- Avoid diagnosis
- Recommend professional consultation
- Provide general guidance only
- End with disclaimer

## RAG Flow

```text
User query
 -> query embedding
 -> Chroma similarity search
 -> context assembly
 -> LLM prompt
 -> structured response + sources
```

## Planned (Not Currently Active)

- Voice STT/TTS pipeline
- Advanced NLP symptom entity extraction
- Prompt-injection guardrail middleware

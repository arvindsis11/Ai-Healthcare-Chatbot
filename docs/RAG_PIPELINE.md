# RAG Pipeline

## Enterprise Retrieval Flow

1. Query normalization and language detection.
2. Embedding generation for semantic retrieval.
3. Vector retrieval from ChromaDB (`top-k`).
4. Hybrid reranking using lexical overlap + retrieval position.
5. Context chunk selection and citation packaging.
6. LLM response generation with symptom analysis context.
7. Medical disclaimer enforcement in response schema.

## Pipeline Diagram

```text
User Query
 -> language detect/normalize
 -> embedding
 -> ChromaDB similarity search
 -> hybrid rerank
 -> chunked context assembly
 -> citation extraction
 -> LLM generation
 -> safe response payload
```

## Safety

- Prompt injection guard before retrieval/generation.
- Triage-aware symptom analysis included in prompt context.
- Non-diagnostic, educational output policy maintained.

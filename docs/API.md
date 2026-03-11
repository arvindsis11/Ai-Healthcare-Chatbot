# API Reference

Base path: `/api/v1`

## `POST /chat`
Main chat endpoint with multilingual handling, triage assessment, citations, and cache.

Request:
```json
{
  "message": "I have fever and headache",
  "conversation_id": "optional-id",
  "symptoms": ["fever", "headache"]
}
```

Response:
```json
{
  "response": "...",
  "conversation_id": "...",
  "sources": ["fever.yml"],
  "citations": [{"id": "fever.yml#chunk-1", "source": "fever.yml", "excerpt": "..."}],
  "symptom_analysis": {
    "symptoms": ["fever", "headache"],
    "severity_score": 5,
    "risk_level": "medium",
    "possible_conditions": ["General symptom cluster requiring clinical correlation"],
    "urgency_recommendation": "Book an appointment with a healthcare professional within 24-72 hours."
  },
  "detected_language": "en",
  "recommended_specialist": "General Physician",
  "disclaimer": "This is not medical advice..."
}
```

## `POST /analyze-symptoms`
Focused symptom analysis endpoint.

## `GET /sessions/{conversation_id}`
Returns persisted in-memory conversation history for anonymous session restoration.

## `GET /health`
Health and feature flags endpoint.

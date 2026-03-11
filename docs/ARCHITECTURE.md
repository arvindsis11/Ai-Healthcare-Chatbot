# 🏗️ System Architecture

This document explains the architecture of the AI Healthcare Chatbot, covering all system layers, component interactions, data flows, and design decisions.

---

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Component Breakdown](#component-breakdown)
  - [Classic Flask Chatbot](#1-classic-flask-chatbot)
  - [FastAPI Voice Backend](#2-fastapi-voice-backend)
  - [Next.js Frontend](#3-nextjs-frontend)
  - [RAG Healthcare Assistant](#4-rag-healthcare-assistant)
- [Data Flow](#data-flow)
  - [Text Chat Flow](#text-chat-flow)
  - [Voice Chat Flow](#voice-chat-flow)
  - [RAG Query Flow](#rag-query-flow)
- [Symptom Analysis Pipeline](#symptom-analysis-pipeline)
- [Training Pipeline](#training-pipeline)
- [Database Design](#database-design)
- [Deployment Architecture](#deployment-architecture)

---

## High-Level Overview

The project is composed of **four distinct layers**, each progressively more sophisticated:

```
┌───────────────────────────────────────────────────────────────────┐
│                          USER LAYER                               │
│   ┌──────────────────────┐     ┌──────────────────────────────┐   │
│   │  Browser (Flask UI)  │     │   Browser (Next.js UI)       │   │
│   │  - Simple HTML/CSS   │     │   - TypeScript + React       │   │
│   │  - jQuery AJAX       │     │   - Tailwind CSS             │   │
│   │  - Text input only   │     │   - Voice + Text input       │   │
│   └──────────┬───────────┘     └──────────────┬───────────────┘   │
└──────────────┼──────────────────────────────── ┼ ─────────────────┘
               │                                 │
               ▼                                 ▼
┌───────────────────────────────────────────────────────────────────┐
│                        BACKEND LAYER                              │
│   ┌──────────────────────┐     ┌──────────────────────────────┐   │
│   │  Flask App (app.py)  │     │   FastAPI (backend/main.py)  │   │
│   │  - GET /             │     │   - POST /api/chat           │   │
│   │  - GET /get?msg=...  │     │   - POST /api/chat/voice     │   │
│   │  ChatterBot Engine   │     │   - GET /api/audio/{file}    │   │
│   │  ListTrainer + YAML  │     │   LLM + Voice Services       │   │
│   └──────────┬───────────┘     └──────────────┬───────────────┘   │
└──────────────┼──────────────────────────────── ┼ ─────────────────┘
               │                                 │
               ▼                                 ▼
┌───────────────────────────────────────────────────────────────────┐
│                     AI / ML SERVICES LAYER                        │
│   ┌─────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│   │   ChatterBot    │  │  OpenAI GPT    │  │ OpenAI Whisper   │  │
│   │   BestMatch     │  │  gpt-3.5-turbo │  │  speech-to-text  │  │
│   │   SQLite store  │  │  LangChain     │  │                  │  │
│   └────────────────-┘  └────────────────┘  └──────────────────┘  │
│                                             ┌──────────────────┐  │
│                                             │   ElevenLabs TTS │  │
│                                             │  text-to-speech  │  │
│                                             └──────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────────┐
│                       RAG PIPELINE LAYER                          │
│   ┌──────────────────────────────────────────────────────────┐    │
│   │  ai-healthcare-assistant/                                 │    │
│   │  ┌────────────────┐   ┌──────────────┐  ┌─────────────┐ │    │
│   │  │ Data Ingestion │──▶│  Embeddings  │─▶│  ChromaDB   │ │    │
│   │  │ (YAML → text)  │   │  (SentTrans) │  │  Vector DB  │ │    │
│   │  └────────────────┘   └──────────────┘  └──────┬──────┘ │    │
│   │                                                 │        │    │
│   │  ┌──────────────────────────────────────────────▼──────┐ │    │
│   │  │   RAG Service: Query → Retrieve → Augment → LLM     │ │    │
│   │  └────────────────────────────────────────────────────-┘ │    │
│   └──────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Classic Flask Chatbot

**Location**: `app.py`, `train.py`, `data/`, `templates/`, `static/`

This is the foundational chatbot built with Flask and ChatterBot.

**Components:**

| File | Purpose |
|------|---------|
| `app.py` | Flask application; routes `/` and `/get` |
| `train.py` | Trains ChatterBot on YAML data files |
| `data/*.yml` | Symptom-specific conversation datasets |
| `templates/index.html` | Chat UI served by Flask |
| `static/style.css` | Dark-themed CSS for the UI |
| `saved_conversations/` | Plain-text logs of all chat sessions |

**Request/Response Flow:**

```
Browser → GET /get?msg=<user_text>
          → ChatterBot.get_response(user_text)
          → returns best match from trained data
          → appended to conversation log file
          → response text returned to browser
```

**Training:**

```
train.py reads all .yml files in data/
         → ListTrainer feeds conversation pairs to ChatterBot
         → stored in db.sqlite3 via SQLAlchemy
```

---

### 2. FastAPI Voice Backend

**Location**: `backend/`

A modern, async FastAPI backend designed for voice-enabled interactions.

**Components:**

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app with all routes |
| `backend/services/llm_service.py` | OpenAI GPT-3.5 via LangChain |
| `backend/services/voice_service.py` | Whisper STT + ElevenLabs TTS |
| `backend/models/chat.py` | Pydantic models for API validation |

**LLM Service Architecture:**

```
User message
    │
    ▼
Medical System Prompt (safety constraints)
    │
    ▼
ChatPromptTemplate (LangChain)
    │
    ▼
ChatOpenAI (gpt-3.5-turbo, temp=0.3)
    │
    ├──▶ Main response text
    │
    └──▶ Symptom Analysis (if keywords detected):
             severity_score (1-10)
             risk_level (low/medium/high)
             possible_conditions []
             urgency_recommendation
```

**Voice Service Architecture:**

```
Audio Upload (webm/wav/mp3/m4a)
    │
    ▼
Prepare Audio (pydub conversion if needed)
    │
    ▼
OpenAI Whisper API (whisper-1)
    │
    ▼
Transcribed text
    │
    ▼
LLM Service (get response)
    │
    ▼
ElevenLabs TTS (generate audio)
    │
    ▼
Temp file → served at /api/audio/{filename}
```

---

### 3. Next.js Frontend

**Location**: `frontend/`

A modern React-based frontend with real-time chat, voice support, and dark mode.

**Component Tree:**

```
app/page.tsx
    └── ChatWindow
            ├── Header (dark mode toggle, menu)
            ├── Sidebar
            │       ├── App settings
            │       ├── Dark mode toggle
            │       └── Clear chat
            ├── Messages area
            │       ├── MessageBubble (user)
            │       └── MessageBubble (assistant)
            ├── Typing indicator (animated dots)
            ├── Audio playback indicator
            └── InputBar
                    ├── Text input
                    └── Voice record button (MediaRecorder API)
```

**State Management:**

```typescript
ChatState {
  messages: Message[]   // All chat messages
  isLoading: boolean    // Waiting for API response
  error?: string        // Error message if any
}

Message {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
}
```

**API Communication:**

```
Text message  → POST /api/chat      → { message, symptom_analysis, timestamp }
Voice message → POST /api/chat/voice (FormData) → { message, audio_url }
Audio file    → GET  /api/audio/{filename}
```

---

### 4. RAG Healthcare Assistant

**Location**: `ai-healthcare-assistant/`

The most advanced module, using Retrieval-Augmented Generation for context-aware responses.

**RAG Pipeline:**

```
YAML Healthcare Data
    │
    ▼
data_ingestion.py
    │  Parses YAML → text chunks
    ▼
Sentence Transformer
    │  text → dense vector embeddings
    ▼
ChromaDB
    │  Stores embeddings + metadata
    ▼

Query Time:
    │
User Query → Sentence Transformer → query vector
    │
    ▼
ChromaDB similarity search → Top-K relevant chunks
    │
    ▼
Context + Query → LLM Prompt → GPT response
```

---

## Data Flow

### Text Chat Flow

```
1. User types a message in the chat UI
2. Frontend sends POST /api/chat with { message: "I have a headache" }
3. FastAPI backend receives the request
4. LLMService constructs a medical prompt with:
   - System instructions (safety constraints)
   - User message
5. OpenAI GPT-3.5-turbo generates a response
6. Symptom keywords are checked (pain, fever, cough, etc.)
7. If symptoms detected → SymptomAnalysis is generated
8. Response { message, symptom_analysis } is returned
9. Frontend renders the assistant message
```

### Voice Chat Flow

```
1. User clicks microphone in the UI
2. Browser MediaRecorder API captures audio as WebM
3. Frontend sends POST /api/chat/voice with audio blob
4. FastAPI saves audio to temp file
5. VoiceService converts audio format if needed (pydub)
6. Whisper API transcribes audio → text
7. LLMService generates response from transcribed text
8. ElevenLabs generates audio from response text
9. Audio saved to temp file, URL returned in response
10. Frontend plays the audio response
11. Temp files are cleaned up in background tasks
```

### RAG Query Flow

```
1. User query arrives at RAG backend
2. Query is embedded using Sentence Transformers
3. ChromaDB performs similarity search (cosine similarity)
4. Top-K most relevant documents retrieved
5. Retrieved context + user query → LLM prompt
6. GPT generates a response grounded in retrieved knowledge
7. Response includes source citations from YAML files
```

---

## Symptom Analysis Pipeline

The symptom analysis is performed by the LLM based on keyword detection:

```python
symptom_keywords = [
    'pain', 'ache', 'hurt', 'sore', 'fever', 'cough', 'nausea',
    'headache', 'dizzy', 'fatigue', 'tired', 'sick', 'ill',
    'symptom', 'feeling', 'stomach', 'chest', 'throat'
]
```

When keywords are detected, a separate LLM call generates a structured JSON analysis:

```json
{
  "severity_score": 4,
  "risk_level": "low",
  "possible_conditions": ["tension headache", "dehydration"],
  "urgency_recommendation": "Monitor symptoms; consult a provider if they worsen."
}
```

**Severity Scale:**

| Score | Level | Meaning |
|-------|-------|---------|
| 1–3 | Mild | Self-care, monitor |
| 4–6 | Moderate | See doctor within days |
| 7–10 | Severe | Seek immediate attention |

---

## Training Pipeline

The classic ChatterBot training pipeline:

```
1. Delete existing db.sqlite3 (fresh start)
2. Initialize ChatBot('Bot')
3. For each .yml file in data/:
   a. Read all lines
   b. Pass to ListTrainer.train()
   c. ChatterBot stores Q→A pairs in SQLite
4. Training complete — bot ready to serve
```

The YAML format used:
```yaml
- - User message (trigger)
  - Bot response
- - Another trigger
  - Another response
```

---

## Database Design

### ChatterBot SQLite Schema

ChatterBot manages its own SQLite database (`db.sqlite3`) using SQLAlchemy:

```
Statement
    ├── id (primary key)
    ├── text (the statement text)
    ├── in_response_to (what triggered this)
    ├── created_at
    └── extra_data (JSON)
```

### Conversation Logs

Plain-text files saved in `saved_conversations/`:

```
bot : Hi There! I am a medical chatbot.
user : I have a headache
bot : Headaches can have many causes...
```

---

## Deployment Architecture

### Local Development

```
[Browser] ←→ [Flask :5000] or [Next.js :3000] ←→ [FastAPI :8000]
```

### Heroku Deployment

```
Procfile: web: gunicorn app:app
```

The Flask app is deployed via Gunicorn on Heroku.

### Docker Compose (Production)

```
                    ┌──────────────────┐
                    │   NGINX Proxy    │
                    └───────┬──────────┘
                    ┌───────┴──────────┐
         ┌──────────▼──────┐  ┌────────▼──────────┐
         │  Next.js :3000  │  │  FastAPI :8000     │
         │  (frontend)     │  │  (backend)         │
         └─────────────────┘  └────────────────────┘
```

See `ai-healthcare-assistant/docker/docker-compose.yml` for the full configuration.

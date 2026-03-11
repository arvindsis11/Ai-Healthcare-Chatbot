# 🏥 AI Healthcare Chatbot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.2.5-green?logo=flask)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)

**An intelligent, conversational AI chatbot for healthcare assistance — built with Python, Flask, FastAPI, and Next.js.**

[📖 Documentation](#-documentation) • [🚀 Quick Start](#-quick-start) • [🤝 Contributing](#-contributing) • [🗺️ Roadmap](#-roadmap)

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Installation Guide](#-installation-guide)
- [Local Development Setup](#-local-development-setup)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [AI / ML Models](#-ai--ml-models)
- [Example Usage](#-example-usage)
- [Screenshots & UI](#-screenshots--ui)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🌟 Project Overview

The **AI Healthcare Chatbot** is a multi-layer conversational AI system designed to assist users with health-related questions and symptom analysis. The project has evolved through several generations:

1. **Classic Chatbot** – A Flask + ChatterBot application trained on custom healthcare YAML datasets. Users can chat via a simple web UI and get symptom-aware responses.
2. **Voice-Enabled Assistant** – A FastAPI backend enhanced with OpenAI Whisper (speech-to-text) and ElevenLabs (text-to-speech), paired with a modern Next.js frontend.
3. **RAG Healthcare Assistant** – An advanced sub-module in `ai-healthcare-assistant/` that uses Retrieval-Augmented Generation (RAG) with ChromaDB vector embeddings for context-aware medical conversations.

> ⚠️ **Medical Disclaimer**: This chatbot provides general health information only. It is **not a substitute for professional medical advice**. Always consult a qualified healthcare provider for any medical concerns.

---

## 🎯 Problem Statement

Access to immediate, reliable health information is a challenge for many people, especially outside of clinic hours. Most individuals turn to search engines for symptom information, often finding inaccurate or alarming content.

This project aims to:
- Provide a friendly, conversational interface for health inquiries
- Guide users through basic symptom assessment
- Recommend appropriate levels of care (self-care vs. doctor visit vs. emergency)
- Offer voice interaction for accessibility
- Always emphasize professional consultation

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Conversational Chat** | Natural language chat powered by ChatterBot and LangChain |
| 🩺 **Symptom Analysis** | Identifies symptoms and provides structured severity assessments |
| 📊 **Risk Triage** | Classifies risk as Low / Medium / High with urgency recommendations |
| 🎤 **Voice Input** | Speech-to-text via OpenAI Whisper |
| 🔊 **Voice Output** | Text-to-speech via ElevenLabs |
| 🔍 **RAG Knowledge Retrieval** | Semantic search over a curated medical knowledge base using ChromaDB |
| 🌙 **Dark Mode** | Toggle between light and dark themes |
| 💾 **Conversation History** | Saves past conversations to local files |
| 🐳 **Docker Support** | Full Docker Compose setup for easy deployment |
| ⚕️ **Medical Safety** | All responses include appropriate disclaimers |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│         (Browser)    Flask HTML UI  /  Next.js Frontend      │
└───────────────┬──────────────────────┬──────────────────────┘
                │                      │
                ▼                      ▼
┌───────────────────────┐  ┌──────────────────────────────────┐
│   Flask App (app.py)  │  │   FastAPI Backend (backend/)     │
│  ─────────────────    │  │  ───────────────────────────     │
│  ChatterBot Engine    │  │  LLM Service (OpenAI GPT)        │
│  YAML Training Data   │  │  Voice Service (Whisper/ElevenLabs)│
│  SQLite Storage       │  │  Symptom Analysis Engine         │
│  Conversation Saver   │  │  REST API Endpoints              │
└───────────────────────┘  └──────────┬───────────────────────┘
                                       │
                           ┌───────────▼───────────┐
                           │  RAG Pipeline          │
                           │  (ai-healthcare-       │
                           │   assistant/)          │
                           │  ──────────────        │
                           │  ChromaDB Vectors      │
                           │  Sentence Transformers │
                           │  Data Ingestion        │
                           └───────────────────────┘
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python 3.8+ | Core language |
| Flask 2.2.5 | Classic chatbot web server |
| FastAPI 0.104 | Modern async API for voice assistant |
| ChatterBot 0.8.4 | Conversational AI engine |
| LangChain | LLM orchestration |
| OpenAI GPT-3.5 | Language model for responses |
| OpenAI Whisper | Speech-to-text transcription |
| ElevenLabs | Text-to-speech synthesis |
| ChromaDB | Vector database for RAG |
| SQLAlchemy | ORM for ChatterBot storage |
| Gunicorn | Production WSGI server |

### Frontend
| Technology | Purpose |
|---|---|
| Next.js 14 | React framework |
| TypeScript | Type-safe JavaScript |
| Tailwind CSS | Utility-first styling |
| Radix UI | Accessible component primitives |
| Lucide React | Icon library |

### Infrastructure
| Technology | Purpose |
|---|---|
| Docker & Docker Compose | Containerized deployment |
| Heroku (Procfile) | Cloud platform deployment |

---

## 📁 Repository Structure

```
Ai-Healthcare-Chatbot/
│
├── app.py                          # Flask chatbot entry point
├── train.py                        # ChatterBot training script
├── requirements.txt                # Root Python dependencies
├── Procfile                        # Heroku deployment config
│
├── data/                           # YAML training datasets
│   ├── greetings.yml               # Greeting conversations
│   ├── fever.yml                   # Fever symptom flows
│   ├── headache.yml                # Headache symptom flows
│   ├── cough.cold.yml              # Cough & cold flows
│   ├── fracture.yml                # Fracture guidance
│   ├── doctor.yml                  # Doctor appointment flows
│   ├── generalhealth.yml           # General health info
│   ├── botprofile.yml              # Bot identity data
│   ├── personalinfo.yml            # Personal info handling
│   └── new.yml                     # Miscellaneous conversations
│
├── templates/
│   └── index.html                  # Flask chat UI template
│
├── static/
│   └── style.css                   # UI styles
│
├── saved_conversations/            # Persisted conversation logs
│
├── backend/                        # FastAPI voice-enabled backend
│   ├── main.py                     # FastAPI app entry point
│   ├── requirements.txt            # Backend dependencies
│   ├── .env.example                # Environment variable template
│   ├── models/
│   │   └── chat.py                 # Pydantic request/response models
│   └── services/
│       ├── llm_service.py          # OpenAI LLM integration
│       └── voice_service.py        # Whisper STT + ElevenLabs TTS
│
├── frontend/                       # Next.js frontend
│   ├── app/
│   │   ├── page.tsx                # Home page
│   │   ├── layout.tsx              # App layout
│   │   └── api/chat/route.ts       # Next.js API route
│   ├── components/
│   │   ├── ChatWindow.tsx          # Main chat component
│   │   ├── InputBar.tsx            # Message input with voice
│   │   ├── MessageBubble.tsx       # Individual message display
│   │   └── Sidebar.tsx             # App sidebar
│   ├── package.json
│   └── tailwind.config.js
│
├── ai-healthcare-assistant/        # Advanced RAG assistant sub-module
│   ├── backend/
│   │   ├── main.py                 # RAG FastAPI backend
│   │   ├── api/chat.py             # Chat API endpoints
│   │   ├── services/
│   │   │   ├── llm_service.py      # LLM with RAG integration
│   │   │   ├── rag_service.py      # RAG orchestration
│   │   │   └── vector_db.py        # ChromaDB wrapper
│   │   ├── rag/data_ingestion.py   # YAML → vector embeddings
│   │   └── config/settings.py      # App configuration
│   ├── frontend/                   # RAG assistant frontend
│   ├── data/                       # Healthcare YAML datasets
│   ├── docker/                     # Docker deployment files
│   ├── scripts/ingest_data.py      # Data ingestion script
│   └── tests/                      # Backend tests
│
└── docs/                           # Project documentation
    ├── ARCHITECTURE.md
    ├── SETUP.md
    ├── AI_MODEL.md
    ├── CONTRIBUTING.md
    └── ROADMAP.md
```

---

## 📦 Installation Guide

### Prerequisites

Make sure you have the following installed:

- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** — [Download Node.js](https://nodejs.org/)
- **Git** — [Download Git](https://git-scm.com/)
- **pip** — comes with Python
- *(Optional)* **Docker** — [Download Docker](https://www.docker.com/)

### Clone the Repository

```bash
git clone https://github.com/arvindsis11/Ai-Healthcare-Chatbot.git
cd Ai-Healthcare-Chatbot
```

---

## 💻 Local Development Setup

### Option A: Classic Flask Chatbot (Simplest)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Train the chatbot
python train.py

# 4. Start the Flask server
python app.py
```

Open your browser at **http://localhost:5000**

---

### Option B: FastAPI Backend + Next.js Frontend (Full Stack)

**Backend setup:**
```bash
cd backend
cp .env.example .env
# Edit .env and add your API keys (OPENAI_API_KEY, ELEVENLABS_API_KEY)

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend setup:**
```bash
cd ../frontend
npm install
```

**Run both servers:**
```bash
# Terminal 1 — Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
cd frontend
npm run dev
```

- Frontend: **http://localhost:3000**
- API Docs: **http://localhost:8000/docs**

---

### Option C: Docker Compose (Recommended for Production)

```bash
cd ai-healthcare-assistant
cp .env.example .env
# Edit .env with your API keys

docker-compose -f docker/docker-compose.yml up --build
```

---

## 🚀 Running the Application

### Flask Chatbot

```bash
python app.py
# Server starts at http://127.0.0.1:5000
```

### FastAPI Backend

```bash
cd backend
uvicorn main:app --reload
# Server starts at http://127.0.0.1:8000
# Swagger docs at http://127.0.0.1:8000/docs
```

### Next.js Frontend

```bash
cd frontend
npm run dev
# App starts at http://localhost:3000
```

### Re-training the Chatbot

If you modify YAML training data, retrain the bot:
```bash
python train.py
```

> ⚠️ This will delete the existing `db.sqlite3` and rebuild from scratch.

---

## 🔌 API Endpoints

### FastAPI Backend (`backend/main.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Detailed service status |
| `POST` | `/api/chat` | Send a text message |
| `POST` | `/api/chat/voice` | Send a voice message (multipart audio) |
| `GET` | `/api/audio/{filename}` | Retrieve a generated audio response |
| `POST` | `/api/voice/stt` | Convert audio to text only |
| `POST` | `/api/voice/tts` | Convert text to audio only |

#### Example: Text Chat

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a headache and slight fever"}'
```

**Response:**
```json
{
  "message": "I'm sorry to hear you're not feeling well...",
  "symptom_analysis": {
    "severity_score": 4,
    "risk_level": "low",
    "possible_conditions": ["tension headache", "viral infection"],
    "urgency_recommendation": "Monitor symptoms and consult a provider if they worsen."
  },
  "audio_url": null
}
```

### Flask Chatbot

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve chat UI |
| `GET` | `/get?msg=<text>` | Get bot response for user text |

---

## 🤖 AI / ML Models

### ChatterBot (Classic Mode)
- **Type**: Retrieval-based conversational model
- **Training data**: Custom YAML files in `data/`
- **Storage**: SQLite via SQLAlchemy
- **Logic adapter**: `BestMatch` – finds the closest matching response from training data

### OpenAI GPT-3.5-Turbo (FastAPI Mode)
- **Type**: Large Language Model (LLM)
- **Integration**: LangChain `ChatOpenAI`
- **Use**: Generates contextual medical responses
- **Temperature**: 0.3 (conservative for medical accuracy)

### OpenAI Whisper
- **Type**: Automatic Speech Recognition (ASR)
- **Model**: `whisper-1`
- **Use**: Converts user voice messages to text

### ElevenLabs TTS
- **Type**: Neural Text-to-Speech
- **Model**: `eleven_monolingual_v1`
- **Use**: Converts bot text responses to natural-sounding speech

### Sentence Transformers (RAG Module)
- **Type**: Embedding model
- **Use**: Converts text to dense vectors for semantic search
- **Storage**: ChromaDB vector database

For detailed model documentation, see [docs/AI_MODEL.md](docs/AI_MODEL.md).

---

## 📝 Example Usage

### Chat via Web UI

1. Open the app in your browser
2. Type a message like: *"I have been having a headache for 2 days"*
3. The bot responds with:
   - General health information
   - Severity assessment
   - Self-care suggestions
   - Recommendation to see a doctor if symptoms persist

### Voice Interaction (FastAPI + Next.js)

1. Click the microphone button in the frontend
2. Speak your symptoms
3. The app transcribes your speech using Whisper
4. GPT generates a response
5. ElevenLabs reads the response aloud

### Example Conversation

```
User: Hi, I've been having a headache for the past two days.

Bot: I'm sorry to hear that. Headaches lasting more than a day can have 
     several causes including tension, dehydration, poor sleep, or eye strain.

     🩺 Symptom Analysis:
     - Severity: 4/10 (Moderate)
     - Risk Level: LOW
     - Possible conditions: Tension headache, Dehydration headache
     - Recommendation: Monitor symptoms. If pain is severe, worsening, 
       or accompanied by vision changes or nausea, please consult a doctor.

     ⚠️ Disclaimer: This is general health information, not medical advice.
```

---

## 🖼️ Screenshots & UI

### Classic Flask Chat Interface

<img width="1918" height="935" alt="Flask Chat UI" src="https://github.com/user-attachments/assets/35ff2918-2947-431a-8f91-212e9c13b560" />

### Modern Next.js Frontend

<img width="1918" height="935" alt="Next.js Frontend" src="https://github.com/user-attachments/assets/854aaadb-2cab-49d1-a3ad-82c625e15dfb" />

**UI Features:**
- Clean dark/light theme toggle
- Real-time typing indicator
- Message bubbles distinguishing user vs. bot
- Sidebar for conversation management
- Symptom analysis panel with risk indicators
- Voice recording button with visual feedback

---

## 🔮 Future Improvements

- [ ] 🏥 **Doctor Recommendation Engine** — Match symptoms to specialties and suggest nearby doctors
- [ ] 🧠 **LLM Fine-tuning** — Fine-tune on medical datasets (MedQA, PubMedQA)
- [ ] 📱 **Mobile App** — React Native or Flutter mobile client
- [ ] 🔐 **User Authentication** — Secure login with conversation history persistence
- [ ] 🌐 **Multi-language Support** — Detect and respond in multiple languages
- [ ] 📈 **Analytics Dashboard** — Track common symptoms and usage patterns
- [ ] 🔗 **EHR Integration** — Connect with electronic health record systems
- [ ] 🚀 **Production Deployment** — AWS/GCP/Azure deployment with CI/CD

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full roadmap.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/Ai-Healthcare-Chatbot.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes** and add tests where applicable
5. **Commit**: `git commit -m "feat: add your feature"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Open a Pull Request** on GitHub

Please read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

---

## 📜 License

This source code is free to use. Note that [ChatterBot](https://github.com/gunthercox/ChatterBot) has its own license which applies when using the ChatterBot component — see the [ChatterBot LICENSE](https://github.com/gunthercox/ChatterBot/blob/master/LICENSE).

All other code in this repository is available under the **MIT License**.

---

## 👤 Author

**Arvind** — [@arvindsis11](https://github.com/arvindsis11)

---

## 📚 Documentation

| Document | Description |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design and component interactions |
| [docs/SETUP.md](docs/SETUP.md) | Detailed environment setup guide |
| [docs/AI_MODEL.md](docs/AI_MODEL.md) | AI/ML models and training details |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to contribute to this project |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Planned features and improvements |

---

<div align="center">
Made with ❤️ for better healthcare accessibility
</div>

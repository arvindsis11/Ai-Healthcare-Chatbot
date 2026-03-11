# 🏥 AI Healthcare Chatbot - RAG Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)

**An intelligent RAG-powered healthcare assistant with semantic search capabilities — built with FastAPI, LangChain, and Next.js.**

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🏗️ Architecture](#-architecture) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Project Overview

The **AI Healthcare Chatbot** is a modern Retrieval-Augmented Generation (RAG) system designed to provide intelligent, context-aware health information through a conversational interface.

This application:
- Uses **ChromaDB** for semantic vector search over medical knowledge bases
- Leverages **OpenAI GPT** for intelligent response generation
- Provides **voice capabilities** (Whisper STT + ElevenLabs TTS)
- Offers a **modern Next.js frontend** for an intuitive user experience
- Emphasizes **medical safety** with appropriate disclaimers

> ⚠️ **Medical Disclaimer**: This chatbot provides general health information only. It is **not a substitute for professional medical advice**. Always consult a qualified healthcare provider for any medical concerns.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Conversational Chat** | Natural language chat with context awareness |
| 🔍 **RAG Knowledge Retrieval** | Semantic search over medical knowledge base using ChromaDB |
| 🩺 **Symptom Analysis** | Identifies symptoms and provides severity assessments |
| 🎤 **Voice Input** | Speech-to-text via OpenAI Whisper |
| 🔊 **Voice Output** | Text-to-speech via ElevenLabs |
| 📊 **Risk Triage** | Classifies risk as Low / Medium / High |
| 🌙 **Dark Mode** | Toggle between light and dark themes |
| 🔐 **Secure API** | FastAPI with CORS protection |
| ⚕️ **Medical Safety** | All responses include appropriate disclaimers |

---

## 🚀 Quick Start

### Prerequisites
- **Python** 3.8+
- **Node.js** 18+
- **npm** 9+
- **API Keys**: OpenAI and ElevenLabs (optional for voice features)

### 1. Clone and Setup

```bash
git clone https://github.com/arvindsis11/Ai-Healthcare-Chatbot.git
cd Ai-Healthcare-Chatbot
chmod +x setup.sh && ./setup.sh
```

### 2. Run Backend

```bash
./run_backend.sh
```

The backend will start on `http://localhost:8000`
- Swagger API documentation: `http://localhost:8000/docs`

### 3. Run Frontend

```bash
./run_frontend.sh
```

The frontend will start on `http://localhost:3000`

### 4. Or Run Everything Together

```bash
./start.sh
```

Access the app at: **http://localhost:3000**

---

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│    Next.js Frontend (UI Layer)      │
│      React + TypeScript + Tailwind  │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│    FastAPI Backend (API Layer)       │
│    - Chat API endpoints              │
│    - Voice service integration       │
│    - RAG orchestration               │
└─────────────────┬────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│  ChromaDB        │  │  OpenAI LLM      │
│  (Vector Store)  │  │  (GPT-3.5)       │
│  Medical Data    │  │                  │
└──────────────────┘  └──────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python 3.8+ | Core language |
| FastAPI 0.104 | Async web framework |
| LangChain | LLM orchestration |
| ChromaDB 0.4 | Vector database |
| OpenAI (GPT-3.5, Whisper) | AI models |
| ElevenLabs | Text-to-speech |
| Pydantic | Data validation |

### Frontend
| Technology | Purpose |
|---|---|
| Next.js 14 | React framework |
| TypeScript | Type-safe JavaScript |
| Tailwind CSS | Styling |
| Radix UI | Component primitives |
| Lucide React | Icons |

---

## 📁 Project Structure

```
Ai-Healthcare-Chatbot/
│
├── backend/                        # FastAPI backend application
│   ├── main.py                     # Application entry point
│   ├── requirements.txt            # Python dependencies
│   ├── api/                        # API routes
│   │   └── chat.py                 # Chat endpoints
│   ├── services/                   # Business logic
│   │   ├── llm_service.py          # LLM integration
│   │   ├── rag_service.py          # RAG orchestration
│   │   └── vector_db.py            # ChromaDB wrapper
│   ├── models/                     # Pydantic models
│   │   └── chat.py                 # Request/response models
│   ├── rag/                        # RAG components
│   │   └── data_ingestion.py       # Vector embedding pipeline
│   ├── config/                     # Configuration
│   │   └── settings.py             # App settings
│   └── utils/                      # Utilities
│       └── text_processing.py      # Text processing helpers
│
├── frontend/                       # Next.js frontend application
│   ├── app/                        # Next.js app directory
│   │   ├── page.tsx                # Home page
│   │   ├── layout.tsx              # Root layout
│   │   └── api/chat/route.ts       # API route
│   ├── components/                 # React components
│   │   ├── ChatWindow.tsx          # Main chat UI
│   │   ├── InputBar.tsx            # Message input
│   │   ├── MessageBubble.tsx       # Message display
│   │   └── Sidebar.tsx             # Navigation
│   ├── package.json                # Dependencies
│   └── tsconfig.json               # TypeScript config
│
├── data/                           # Healthcare YAML datasets
│   ├── greetings.yml               # Greeting flows
│   ├── fever.yml                   # Fever guidance
│   ├── headache.yml                # Headache flows
│   └── ...                         # Other symptom datasets
│
├── scripts/                        # Utility scripts
│   └── ingest_data.py              # Data ingestion script
│
├── tests/                          # Test suite
│   └── test_backend.py             # Backend tests
│
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md             # System design
│   └── SETUP.md                    # Detailed setup guide
│
├── setup.sh                        # Automated setup script
├── run_backend.sh                  # Backend startup
├── run_frontend.sh                 # Frontend startup
├── start.sh                        # Full-stack startup
├── requirements.txt                # Root dependencies
└── README.md                       # This file
```

---

## 🔧 Development Setup

### Backend Development

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Configure environment** (create `.env` file in `backend/`):
```env
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
ELEVENLABS_MODEL_ID=eleven_monolingual_v1
DATABASE_URL=sqlite:///./chatbot.db
CHROMADB_PATH=./chroma_db
```

**Run development server**:
```bash
python main.py
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

---

## 📚 API Endpoints

### Chat Endpoints

**POST** `/api/chat`
- Request: `{ "message": "string", "session_id": "string" }`
- Response: `{ "response": "string", "sources": [...] }`

**GET** `/health`
- Response: `{ "status": "ok" }`

**GET** `/docs`
- Interactive Swagger API documentation

---

## 🧠 How It Works

1. **User Input**: User types or speaks a health question
2. **Text Processing**: Input is normalized and cleaned
3. **Vector Embedding**: Question is converted to embeddings
4. **Semantic Search**: ChromaDB retrieves relevant medical documents
5. **LLM Processing**: Retrieved context + question sent to OpenAI GPT
6. **Response Generation**: LLM generates a safe, informed response
7. **Output**: Response displayed and optionally converted to speech

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Arvind Singh** - [@arvindsis11](https://github.com/arvindsis11)

---

**Last Updated**: March 2026  
**Version**: 2.0 (RAG-focused restructure)

# 🛠️ Setup Guide

This guide provides detailed, step-by-step instructions for setting up the AI Healthcare Chatbot on your local machine.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Option A: Classic Flask Chatbot](#option-a-classic-flask-chatbot)
- [Option B: FastAPI + Next.js Full Stack](#option-b-fastapi--nextjs-full-stack)
- [Option C: RAG Healthcare Assistant](#option-c-rag-healthcare-assistant)
- [Option D: Docker Compose](#option-d-docker-compose)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Download |
|----------|----------------|----------|
| Python | 3.8+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| npm | 9+ | Comes with Node.js |
| Git | Any | https://git-scm.com/ |

### Optional Software

| Software | Purpose | Download |
|----------|---------|----------|
| Docker | Container-based deployment | https://www.docker.com/ |
| Docker Compose | Multi-container orchestration | Bundled with Docker Desktop |

### API Keys (for FastAPI/RAG modes only)

| Service | Required For | Get Key |
|---------|-------------|---------|
| OpenAI API Key | GPT responses + Whisper STT | https://platform.openai.com/ |
| ElevenLabs API Key | Text-to-Speech audio responses | https://elevenlabs.io/ |

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/arvindsis11/Ai-Healthcare-Chatbot.git
cd Ai-Healthcare-Chatbot
```

---

## Option A: Classic Flask Chatbot

This is the simplest setup. No API keys required.

### 1.1 Create a Virtual Environment

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt when activated.

### 1.2 Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.2.5
- ChatterBot 0.8.4
- SQLAlchemy
- Gunicorn 22.0.0

### 1.3 Train the Chatbot

```bash
python train.py
```

Expected output:
```
No database found. Creating new database.
Training using greetings.yml
Training completed for greetings.yml
Training using fever.yml
Training completed for fever.yml
...
```

> ⚠️ If you see `Old database removed. Training new database.`, that's normal — it deletes and rebuilds the SQLite database.

### 1.4 Start the Flask Server

```bash
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 1.5 Open the App

Open your browser and navigate to: **http://localhost:5000**

---

## Option B: FastAPI + Next.js Full Stack

### 2.1 Backend Setup

```bash
cd backend
```

**Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
OPENAI_API_KEY=sk-your-openai-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
ELEVENLABS_MODEL_ID=eleven_monolingual_v1
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

**Start the FastAPI server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

Swagger API docs: **http://localhost:8000/docs**

### 2.2 Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
```

**Start the development server:**
```bash
npm run dev
```

Expected output:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
- Ready in 2s
```

Open your browser: **http://localhost:3000**

---

## Option C: RAG Healthcare Assistant

### 3.1 Setup

```bash
cd ai-healthcare-assistant
cp .env.example .env
# Edit .env with your API keys
```

### 3.2 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.3 Ingest Training Data

This creates vector embeddings from the YAML healthcare data:

```bash
cd ..
python scripts/ingest_data.py
```

Expected output:
```
Loading data from data/ directory...
Processing greetings.yml...
Processing fever.yml...
...
Embeddings created and stored in ChromaDB
Data ingestion complete!
```

### 3.4 Run RAG Backend

```bash
cd backend
python main.py
```

### 3.5 Run RAG Frontend

```bash
cd ../frontend
npm install
npm run dev
```

---

## Option D: Docker Compose

This runs the full stack (backend + frontend) in containers.

### 4.1 Prerequisites

- Docker Desktop installed and running
- API keys ready

### 4.2 Setup Environment

```bash
cd ai-healthcare-assistant
cp .env.example .env
# Edit .env with your API keys
```

### 4.3 Build and Run

```bash
docker-compose -f docker/docker-compose.yml up --build
```

This will:
1. Build the Python backend image
2. Build the Next.js frontend image
3. Start both services

Expected output:
```
Creating network...
Building backend...
Building frontend...
Starting ai-healthcare-assistant_backend_1 ... done
Starting ai-healthcare-assistant_frontend_1 ... done
```

Services:
- Frontend: **http://localhost:3000**
- Backend API: **http://localhost:8000**
- API Docs: **http://localhost:8000/docs**

### 4.4 Stop Services

```bash
docker-compose -f docker/docker-compose.yml down
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | — | OpenAI API key for GPT + Whisper |
| `ELEVENLABS_API_KEY` | ⚠️ Optional | — | ElevenLabs for text-to-speech |
| `ELEVENLABS_VOICE_ID` | No | `21m00Tcm4TlvDq8ikWAM` | Voice ID (Rachel) |
| `ELEVENLABS_MODEL_ID` | No | `eleven_monolingual_v1` | TTS model |
| `HOST` | No | `0.0.0.0` | Server bind address |
| `PORT` | No | `8000` | Server port |
| `CORS_ORIGINS` | No | `*` | Allowed CORS origins |

> 🔒 **Security**: Never commit your `.env` file to Git. It is listed in `.gitignore`.

---

## Troubleshooting

### Python Issues

**Problem**: `ModuleNotFoundError: No module named 'chatterbot'`
```bash
# Make sure your virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Problem**: ChatterBot installation fails
```bash
# Try installing with the --no-deps flag
pip install chatterbot==0.8.4 --no-deps
pip install pyaml pint nltk
```

**Problem**: SQLAlchemy version conflict
```bash
pip install SQLAlchemy==1.4.46
```

---

### Node.js Issues

**Problem**: `npm install` fails with peer dependency errors
```bash
npm install --legacy-peer-deps
```

**Problem**: Next.js port 3000 already in use
```bash
# Kill the process on port 3000
lsof -ti:3000 | xargs kill -9   # macOS/Linux
netstat -ano | findstr :3000      # Windows (find PID, then kill)

# Or run on a different port
npm run dev -- -p 3001
```

---

### FastAPI Issues

**Problem**: `OPENAI_API_KEY` not found
```bash
# Make sure .env file exists and has the correct key
cat backend/.env
# Should show: OPENAI_API_KEY=sk-...
```

**Problem**: Port 8000 already in use
```bash
uvicorn main:app --reload --port 8001
```

**Problem**: CORS errors in browser
- Make sure `CORS_ORIGINS` in `.env` includes your frontend URL
- Default allows all origins (`*`) for development

---

### Docker Issues

**Problem**: `docker-compose` command not found
```bash
# Docker Desktop includes Docker Compose v2
docker compose up --build    # Note: no hyphen in newer versions
```

**Problem**: Build fails due to missing API key
```bash
# Ensure .env file exists with valid keys
cat ai-healthcare-assistant/.env
```

**Problem**: Container port conflict
```bash
# Check what's using the port
docker ps
# Stop conflicting container
docker stop <container_id>
```

---

### Training Issues

**Problem**: `FileNotFoundError: db.sqlite3` when running `app.py` without training
```bash
# Always run train.py before app.py
python train.py
python app.py
```

**Problem**: Chatbot gives unrelated responses
```bash
# Retrain the bot with cleaned data
python train.py
```

**Problem**: `saved_conversations/` directory issues
```bash
# Create the directory if missing
mkdir saved_conversations
echo "0" > saved_conversations/0
```

---

### Getting Help

If you encounter issues not listed here:

1. Check [GitHub Issues](https://github.com/arvindsis11/Ai-Healthcare-Chatbot/issues)
2. Open a new issue with:
   - Your operating system
   - Python version (`python --version`)
   - Node.js version (`node --version`)
   - Error message (full stack trace)
   - Steps to reproduce

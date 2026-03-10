# AI Healthcare Assistant

A modern, production-ready AI healthcare chatbot built with FastAPI, React, and Retrieval-Augmented Generation (RAG).

## Architecture Overview

### Backend (`/backend`)
- **Framework**: FastAPI for high-performance async API
- **LLM Integration**: OpenAI GPT models with LangChain
- **Vector Database**: ChromaDB for document embeddings
- **RAG Pipeline**: Semantic search with context-aware responses
- **Data Processing**: YAML conversation data converted to vector embeddings

### Frontend (`/frontend`)
- **Framework**: Next.js 14 with React 18
- **Styling**: Tailwind CSS for modern UI
- **Components**: ChatGPT-style interface with real-time messaging
- **State Management**: React hooks for chat state

### Data Pipeline (`/data`, `/embeddings`)
- **Source Data**: YAML files with healthcare conversations
- **Embeddings**: Sentence transformers for semantic search
- **Vector Storage**: ChromaDB for persistent vector storage

## Features

- 🤖 AI-powered healthcare conversations
- 🔍 Semantic search over medical knowledge base
- 💬 ChatGPT-style interface
- 🚀 Production-ready with Docker
- 📱 Responsive design
- ⚡ Real-time responses

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### Installation

1. **Clone and setup:**
   ```bash
   cd ai-healthcare-assistant
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

2. **Backend setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend setup:**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Data ingestion:**
   ```bash
   cd ..
   python scripts/ingest_data.py
   ```

5. **Run the application:**
   ```bash
   # Terminal 1: Backend
   cd backend
   python main.py

   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

6. **Open browser:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Docker Deployment

```bash
docker-compose -f docker/docker-compose.yml up --build
```

## Project Structure

```
ai-healthcare-assistant/
├── backend/                    # FastAPI backend
│   ├── api/                    # API endpoints
│   │   └── chat.py            # Chat endpoints
│   ├── services/              # Business logic
│   │   ├── llm_service.py     # OpenAI integration
│   │   ├── vector_db.py       # ChromaDB wrapper
│   │   └── rag_service.py     # RAG orchestration
│   ├── models/                # Pydantic models
│   │   └── chat.py           # Request/Response models
│   ├── rag/                  # RAG pipeline
│   │   └── data_ingestion.py # Data processing
│   ├── utils/                # Utilities
│   │   └── text_processing.py # Text processing helpers
│   ├── config/               # Configuration
│   │   └── settings.py       # App settings
│   └── main.py               # FastAPI app
├── frontend/                  # Next.js frontend
│   ├── components/           # React components
│   │   ├── ChatInterface.tsx # Main chat component
│   │   ├── MessageBubble.tsx # Message display
│   │   └── ChatInput.tsx     # Input component
│   ├── pages/                # Next.js pages
│   │   ├── _app.tsx         # App wrapper
│   │   └── index.tsx        # Home page
│   ├── hooks/               # Custom hooks
│   │   └── useChat.ts       # Chat logic hook
│   └── styles/              # Styles
│       └── globals.css      # Global styles
├── data/                     # Training data
├── embeddings/               # Vector database
├── docker/                   # Docker files
├── scripts/                  # Utility scripts
│   └── ingest_data.py       # Data ingestion
└── tests/                    # Test files
```

## API Documentation

### POST /api/v1/chat
Send a chat message and receive AI response.

**Request:**
```json
{
  "message": "What are the symptoms of fever?",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**
```json
{
  "response": "Fever symptoms include high body temperature...",
  "conversation_id": "conversation-id",
  "sources": ["fever.yml"]
}
```

## Development

### Backend Development
- Uses FastAPI with automatic API documentation
- Pydantic models for type validation
- Dependency injection for services
- Async endpoints for scalability

### Frontend Development
- Next.js with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Custom hooks for state management

### Data Pipeline
- YAML files processed into vector embeddings
- ChromaDB for vector storage and similarity search
- Sentence transformers for embedding generation

## Deployment

### Local Development
Use Docker Compose for full stack development.

### Production
- Backend: Deploy to cloud (AWS, GCP, Azure)
- Frontend: Deploy to Vercel, Netlify, or cloud storage
- Database: Use managed ChromaDB or Pinecone for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
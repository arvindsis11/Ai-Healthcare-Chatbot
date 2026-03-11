from fastapi import APIRouter, HTTPException, Depends
from ..models.chat import ChatRequest, ChatResponse
from ..services.rag_service import RAGService
from ..config.settings import settings
from datetime import datetime
import uuid

router = APIRouter()

# Global service instances (in production, use proper DI)
_rag_service = None

def get_rag_service() -> RAGService:
    global _rag_service
    if _rag_service is None:
        from ..services.vector_db import VectorDatabase
        from ..services.llm_service import LLMService
        from ..services.rag_service import RAGService

        vector_db = VectorDatabase(
            persist_directory=settings.chroma_persist_directory,
            collection_name=settings.chroma_collection_name
        )

        llm_service = LLMService(
            api_key=settings.openai_api_key,
            model=settings.openai_model
        )

        _rag_service = RAGService(vector_db, llm_service)

    return _rag_service

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
) -> ChatResponse:
    """Enhanced chat endpoint with symptom analysis and medical RAG."""
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Use enhanced RAG query with symptom analysis
        result = rag_service.query_with_symptoms(
            request.message,
            request.symptoms
        )

        return ChatResponse(
            response=result['response'],
            conversation_id=conversation_id,
            sources=result.get('sources', []),
            symptom_analysis=result.get('symptom_analysis')
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.post("/analyze-symptoms", response_model=ChatResponse)
async def analyze_symptoms(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
) -> ChatResponse:
    """Dedicated endpoint for symptom analysis."""
    try:
        if not request.symptoms and not request.message:
            raise HTTPException(status_code=400, detail="Either symptoms or message must be provided")

        # Extract symptoms if not provided explicitly
        symptoms = request.symptoms or rag_service.extract_symptoms_from_text(request.message)

        if not symptoms:
            return ChatResponse(
                response="I couldn't identify any specific symptoms in your message. Please provide more details about what you're experiencing.",
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                symptom_analysis=None
            )

        # Perform full analysis
        result = rag_service.query_with_symptoms(
            request.message or f"I have these symptoms: {', '.join(symptoms)}",
            symptoms
        )

        return ChatResponse(
            response=result['response'],
            conversation_id=request.conversation_id or str(uuid.uuid4()),
            sources=result.get('sources', []),
            symptom_analysis=result.get('symptom_analysis')
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing symptoms: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "features": ["symptom_analysis", "rag", "medical_assistant"]
    }
import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request

from ..ai.prompt_guard import is_prompt_injection
from ..ai.translation_service import TranslationService
from ..core.dependencies import (
    get_cache,
    get_doctor_recommendation_service,
    get_rag_service,
    get_session_repository,
    get_symptom_extraction_service,
    get_translation_service,
    get_triage_service,
)
from ..models.chat import ChatRequest, ChatResponse
from ..repositories.session_repository import SessionRepository
from ..services.cache_service import chat_cache_key
from ..services.medical_intelligence_service import (
    DoctorRecommendationService,
    SymptomExtractionService,
    TriageService,
)
from ..services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request_ctx: Request,
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
    session_repository: SessionRepository = Depends(get_session_repository),
    cache = Depends(get_cache),
    translation_service: TranslationService = Depends(get_translation_service),
    symptom_extractor: SymptomExtractionService = Depends(get_symptom_extraction_service),
    triage_service: TriageService = Depends(get_triage_service),
    doctor_service: DoctorRecommendationService = Depends(get_doctor_recommendation_service),
) -> ChatResponse:
    """Enhanced chat endpoint with symptom analysis and medical RAG."""
    try:
        if is_prompt_injection(request.message):
            raise HTTPException(status_code=400, detail="Prompt appears unsafe and was blocked")

        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        request_id = getattr(request_ctx.state, "request_id", "unknown")

        detected_language = translation_service.detect_language(request.message)
        normalized_message = (
            translation_service.translate_to_english(request.message, detected_language)
            if detected_language != "en"
            else request.message
        )

        symptoms = symptom_extractor.extract(normalized_message, request.symptoms)
        rule_based_analysis = triage_service.assess(symptoms)
        doctor_recommendation = doctor_service.recommend_detailed(symptoms)
        recommended_specialist = doctor_recommendation.specialist

        cache_key = chat_cache_key(normalized_message)
        cached = cache.get(cache_key)
        if cached:
            session_repository.append_message(conversation_id, "user", request.message)
            session_repository.append_message(conversation_id, "assistant", cached["response"])
            return ChatResponse(
                response=cached["response"],
                conversation_id=conversation_id,
                sources=cached.get("sources", []),
                citations=cached.get("citations", []),
                symptom_analysis=rule_based_analysis,
                detected_language=detected_language,
                recommended_specialist=recommended_specialist,
                doctor_recommendation=doctor_recommendation,
            )

        # Use enhanced RAG query with symptom analysis
        result = rag_service.query_with_symptoms(
            normalized_message,
            symptoms,
        )

        response_text = result["response"]
        if detected_language != "en":
            response_text = translation_service.translate_from_english(response_text, detected_language)

        cache.set(
            cache_key,
            {
                "response": response_text,
                "sources": result.get("sources", []),
                "citations": result.get("citations", []),
            },
        )

        session_repository.append_message(conversation_id, "user", request.message)
        session_repository.append_message(conversation_id, "assistant", response_text)

        logger.info(
            "chat_request_processed",
            extra={
                "request_id": request_id,
                "endpoint": "/api/v1/chat",
                "latency_ms": None,
            },
        )

        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            sources=result.get("sources", []),
            citations=result.get("citations", []),
            symptom_analysis=result.get("symptom_analysis") or rule_based_analysis,
            detected_language=detected_language,
            recommended_specialist=recommended_specialist,
            doctor_recommendation=doctor_recommendation,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error processing chat request: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing chat request")

@router.post("/analyze-symptoms", response_model=ChatResponse)
async def analyze_symptoms(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
    symptom_extractor: SymptomExtractionService = Depends(get_symptom_extraction_service),
    triage_service: TriageService = Depends(get_triage_service),
    doctor_service: DoctorRecommendationService = Depends(get_doctor_recommendation_service),
) -> ChatResponse:
    """Dedicated endpoint for symptom analysis."""
    try:
        if not request.symptoms and not request.message:
            raise HTTPException(status_code=400, detail="Either symptoms or message must be provided")

        # Extract symptoms if not provided explicitly
        symptoms = symptom_extractor.extract(request.message, request.symptoms)

        if not symptoms:
            return ChatResponse(
                response="I couldn't identify any specific symptoms in your message. Please provide more details about what you're experiencing.",
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                symptom_analysis=None,
                recommended_specialist="General Physician",
            )

        # Perform full analysis
        result = rag_service.query_with_symptoms(
            request.message or f"I have these symptoms: {', '.join(symptoms)}",
            symptoms,
        )
        triage = triage_service.assess(symptoms)

        doctor_recommendation = doctor_service.recommend_detailed(symptoms)
        return ChatResponse(
            response=result["response"],
            conversation_id=request.conversation_id or str(uuid.uuid4()),
            sources=result.get("sources", []),
            citations=result.get("citations", []),
            symptom_analysis=result.get("symptom_analysis") or triage,
            recommended_specialist=doctor_recommendation.specialist,
            doctor_recommendation=doctor_recommendation,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error analyzing symptoms: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error analyzing symptoms")

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "features": [
            "symptom_analysis",
            "rag",
            "medical_assistant",
            "cache",
            "session_persistence",
            "prompt_guard",
        ],
    }


@router.get("/sessions/{conversation_id}")
async def get_session_history(
    conversation_id: str,
    session_repository: SessionRepository = Depends(get_session_repository),
):
    messages = session_repository.get_messages(conversation_id)
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }
from functools import lru_cache

from ..ai.translation_service import TranslationService
from ..repositories.session_repository import SessionRepository
from ..repositories.vector_db import VectorDatabase
from ..services.cache_service import CompositeCache, InMemoryTTLCache, RedisCache
from ..services.llm_service import LLMService
from ..services.medical_intelligence_service import (
    DoctorRecommendationService,
    SymptomExtractionService,
    TriageService,
)
from ..services.health_report_service import HealthReportService
from ..services.rag_service import RAGService
from .settings import settings


@lru_cache
def get_vector_db() -> VectorDatabase:
    return VectorDatabase(
        persist_directory=settings.chroma_persist_directory,
        collection_name=settings.chroma_collection_name,
    )


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService(api_key=settings.openai_api_key, model=settings.openai_model)


@lru_cache
def get_rag_service() -> RAGService:
    return RAGService(get_vector_db(), get_llm_service())


@lru_cache
def get_translation_service() -> TranslationService:
    return TranslationService(api_key=settings.openai_api_key)


@lru_cache
def get_symptom_extraction_service() -> SymptomExtractionService:
    return SymptomExtractionService()


@lru_cache
def get_triage_service() -> TriageService:
    return TriageService()


@lru_cache
def get_doctor_recommendation_service() -> DoctorRecommendationService:
    return DoctorRecommendationService()


@lru_cache
def get_session_repository() -> SessionRepository:
    return SessionRepository()


@lru_cache
def get_health_report_service() -> HealthReportService:
    return HealthReportService(get_session_repository(), get_llm_service())


@lru_cache
def get_cache() -> CompositeCache:
    return CompositeCache(
        primary=RedisCache(redis_url=settings.redis_url, ttl_seconds=settings.cache_ttl_seconds),
        fallback=InMemoryTTLCache(ttl_seconds=settings.cache_ttl_seconds),
    )

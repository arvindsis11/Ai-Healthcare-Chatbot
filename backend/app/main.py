import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.chat import router as chat_router
from .api.reports import router as reports_router
from .core.logging import configure_logging
from .core.llm_provider import resolve_base_url, validate_provider_connectivity
from .core.settings import settings
from .middleware.request_context import RequestContextMiddleware
from .middleware.security import InMemoryRateLimiter, SecurityMiddleware


configure_logging()
logger = logging.getLogger(__name__)

# Log active provider and validate connectivity for local providers
_resolved_base_url = resolve_base_url(settings.llm_provider, settings.openai_base_url)
logger.info("LLM provider: %s", settings.llm_provider)
if _resolved_base_url:
    validate_provider_connectivity(settings.llm_provider, _resolved_base_url)


app = FastAPI(
    title=settings.app_name,
    description="AI Healthcare Assistant API",
    version="1.0.0",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    SecurityMiddleware,
    limiter=InMemoryRateLimiter(requests_per_minute=settings.rate_limit_per_minute),
    max_body_size=settings.request_size_limit_bytes,
)

app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(reports_router, prefix="/api/v1", tags=["reports"])


@app.get("/")
async def root():
    return {"message": "AI Healthcare Assistant API", "version": "1.0.0"}

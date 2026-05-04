from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.chat import router as chat_router
from .api.reports import router as reports_router
from .api.face_analysis import router as face_analysis_router
from .core.logging import configure_logging
from .core.settings import settings
from .middleware.request_context import RequestContextMiddleware
from .middleware.security import InMemoryRateLimiter, SecurityMiddleware


configure_logging()


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
app.include_router(face_analysis_router, prefix="/api/v1", tags=["face-analysis"])


@app.get("/")
async def root():
    return {"message": "AI Healthcare Assistant API", "version": "1.0.0"}

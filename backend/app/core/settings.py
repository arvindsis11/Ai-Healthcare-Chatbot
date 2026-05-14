from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # LLM Provider
    # Supported values: "openai", "lm-studio", "ollama"
    llm_provider: Literal["openai", "lm-studio", "ollama"] = "openai"

    # OpenAI / local LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    # Base URL for the chat-completions endpoint.
    # Leave blank to use the provider default:
    #   openai    -> https://api.openai.com/v1
    #   lm-studio -> http://localhost:1234/v1
    #   ollama    -> http://localhost:11434/v1
    openai_base_url: str = ""
    # Request timeout in seconds for LLM API calls.
    # 0 means use the provider default:
    #   openai    -> 30s  (fast API; a hang almost always means an error)
    #   lm-studio -> 120s (local inference can be slow, especially on first run)
    #   ollama    -> 120s
    llm_timeout_seconds: int = 0

    # ChromaDB
    chroma_persist_directory: str = "./embeddings"
    chroma_collection_name: str = "healthcare_docs"

    # App
    app_name: str = "AI Healthcare Assistant"
    debug: bool = False

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Security
    rate_limit_per_minute: int = 60
    request_size_limit_bytes: int = 65536

    # Persistence and cache
    database_url: str = ""
    redis_url: str = ""
    cache_ttl_seconds: int = 300

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        case_sensitive=False,
    )

settings = Settings()
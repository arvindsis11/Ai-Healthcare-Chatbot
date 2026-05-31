from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Path to the .env file, shared by load_dotenv (below) and pydantic-settings.
_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"

# Load the .env file into os.environ as well. pydantic-settings only maps the
# variables declared on Settings; libraries that read os.environ directly —
# notably LiteLLM looking up ANTHROPIC_API_KEY / GEMINI_API_KEY / etc. — need
# the values exported to the process environment too.
# override=False keeps real environment variables (e.g. those set by Docker)
# authoritative over the .env file.
load_dotenv(_ENV_FILE, override=False)


class Settings(BaseSettings):
    # LLM Provider
    # Supported values: "openai", "lm-studio", "ollama", "litellm"
    llm_provider: Literal["openai", "lm-studio", "ollama", "litellm"] = "openai"

    # OpenAI / local LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    # Base URL for the chat-completions endpoint.
    # Leave blank to use the provider default:
    #   openai    -> https://api.openai.com/v1
    #   lm-studio -> http://localhost:1234/v1
    #   ollama    -> http://localhost:11434/v1
    #   litellm   -> not used (LiteLLM routes internally via the model string)
    openai_base_url: str = ""
    # Request timeout in seconds for LLM API calls.
    # 0 means use the provider default:
    #   openai    -> 30s  (fast API; a hang almost always means an error)
    #   lm-studio -> 120s (local inference can be slow, especially on first run)
    #   ollama    -> 120s
    #   litellm   -> 60s
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
        env_file=str(_ENV_FILE),
        case_sensitive=False,
    )

settings = Settings()
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"

    # ChromaDB
    chroma_persist_directory: str = "./embeddings"
    chroma_collection_name: str = "healthcare_docs"

    # App
    app_name: str = "AI Healthcare Assistant"
    debug: bool = False

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        case_sensitive=False,
    )

settings = Settings()
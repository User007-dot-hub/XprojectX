"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    GEMINI_API_KEY: str = ""
    MODEL_DIR: str = "models"
    DATA_CACHE_DIR: str = "cache"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


# Singleton settings instance
settings = Settings()

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o"
    openai_temperature: float = 0.4
    openai_max_tokens: int = 1024

    # API Configuration
    api_key: Optional[str] = None  # For authentication
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Rate Limiting
    rate_limit_requests: int = 10
    rate_limit_window: int = 60  # seconds

    # File Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list[str] = ["application/pdf", "application/x-pdf"]

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
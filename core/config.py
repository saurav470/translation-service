
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Translation Service"
    VERSION: str = "1.0.0"
    

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-5"
    

    MAX_TEXT_LENGTH: int = 10000
    SUPPORTED_LANGUAGES: List[str] = ["swedish", "dutch"]
    DEFAULT_LANGUAGE: str = "swedish"
    

    MIN_QUALITY_SCORE: int = 70
    PROFESSIONAL_QUALITY_SCORE: int = 85
    PUBLICATION_QUALITY_SCORE: int = 95
    

    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./langTranslator.db")
    

    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()


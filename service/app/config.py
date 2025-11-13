"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        database_url: Database connection URL.
        debug: Enable debug mode.
        session_max_age_seconds: Maximum session age in seconds (1 hour).
        secret_key: Secret key for session token generation.
    """
    database_url: str = "sqlite:///./banking_service.db"
    debug: bool = False
    session_max_age_seconds: int = 3600  # 1 hour
    secret_key: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


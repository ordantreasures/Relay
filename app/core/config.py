# # app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Security
     #CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
        # CORS - Special handling for Railway
    @property
    def cors_origins(self):
        if self.ENVIRONMENT == "production":
            return ["https://relaey.netlify.app"]
        return ["http://localhost:3000", "http://localhost:8000"]
    
    # App
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    model_config = {
        "env_file": ".env"  if os.path.exists(".env") else None,
        "case_sensitive": False
    }

settings = Settings() #type: ignore
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Backend Configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    DEBUG: bool = False

    # Database Configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "chatbot_user"
    POSTGRES_PASSWORD: str = "secure_password"
    POSTGRES_DB: str = "chatbot_db"

    # Vector Database Configuration
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "textbook_content"

    # AI Service Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-pro"

    # Application Settings
    TEXTBOOK_CONTENT_PATH: str = "../website/docs"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    MAX_RETRIEVAL_RESULTS: int = 5
    RESPONSE_TIMEOUT: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
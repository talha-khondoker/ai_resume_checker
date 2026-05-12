"""
Application configuration management.
"""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Info
    API_TITLE: str = "AI Resume Analyzer API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Analyze and match resumes with job descriptions using AI/ML"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_FOLDER: str = "app/uploads"
    ALLOWED_EXTENSIONS: str = "pdf,docx"
    
    # Email
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # ML Model
    SPACY_MODEL: str = "en_core_web_sm"
    SIMILARITY_THRESHOLD: float = 0.6
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse ALLOWED_ORIGINS into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Parse ALLOWED_EXTENSIONS into a list."""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Load settings
settings = Settings()

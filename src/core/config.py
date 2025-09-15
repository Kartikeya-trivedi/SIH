from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Kolam Learning Platform"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database
    database_url: str = "sqlite:///./kolam.db"
    database_url_test: str = "sqlite:///./kolam_test.db"
    
    # OpenSearch
    opensearch_url: str = "http://localhost:9200"
    opensearch_username: Optional[str] = None
    opensearch_password: Optional[str] = None
    
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File Storage
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: str = "jpg,jpeg,png,gif,svg"
    
    # AI Model Configuration
    model_path: str = "models/"
    detection_confidence_threshold: float = 0.7
    generation_max_complexity: int = 100
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    enable_tracing: bool = True
    jaeger_endpoint: str = "http://localhost:14268/api/traces"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


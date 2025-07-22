import os
import yaml
from typing import Dict, Any
from pydantic import BaseModel

class GeminiConfig(BaseModel):
    model: str = "gemini-1.5-pro"
    temperature: float = 0.1
    max_tokens: int = 8192
    max_conversation: int = 50

class EmbeddingsConfig(BaseModel):
    model: str = "text-embedding-004"
    dimensions: int = 768

class AppConfig(BaseModel):
    gemini: GeminiConfig = GeminiConfig()
    embeddings: EmbeddingsConfig = EmbeddingsConfig()

def load_config() -> AppConfig:
    """Load configuration from environment variables and defaults."""
    return AppConfig()

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "legabot_db")
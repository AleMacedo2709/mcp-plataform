from pathlib import Path
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Carrega arquivo .env específico por ambiente
ENV = os.getenv("ENVIRONMENT", "local").lower()
env_file = os.getenv("ENV_FILE", f".env.{ENV}")

  # fallback

class Settings(BaseModel):
    ENVIRONMENT: str = ENV
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/projects_db")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

settings = Settings()

# Load shared env only
try:
    _root_env = Path(__file__).resolve().parents[3] / '.env.shared'
    load_dotenv(str(_root_env), override=True)
except Exception:
    pass

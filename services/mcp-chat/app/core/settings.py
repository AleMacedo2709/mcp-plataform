from pydantic import BaseModel
import os
from dotenv import load_dotenv

ENV = os.getenv("ENVIRONMENT", "local").lower()
env_file = os.getenv("ENV_FILE", f".env.{ENV}")



class Settings(BaseModel):
    ENVIRONMENT: str = ENV
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/projects_db")
    RESOURCE_DIR: str = os.getenv("RESOURCE_DIR", "/data/resources")
    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "openrouter/anthropic/claude-3.5-sonnet")

settings = Settings()

try:
    _root_env = Path(__file__).resolve().parents[3] / '.env.shared'
    , override=False)
except Exception:
    pass

# Load shared env only
try:
    _root_env = Path(__file__).resolve().parents[3] / '.env.shared'
    load_dotenv(str(_root_env), override=True)
except Exception:
    pass

from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pathlib import Path

ENV = os.getenv("ENVIRONMENT", "local").lower()
env_file = os.getenv("ENV_FILE", f".env.{ENV}")



class Settings(BaseModel):
    ENVIRONMENT: str = ENV
    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "openrouter/anthropic/claude-3.5-sonnet")
    ALLOW_DEMO: bool = os.getenv("ALLOW_DEMO", "true").lower() == "true"
    MAX_FILE_MB: int = int(os.getenv("MAX_FILE_MB", "50"))

settings = Settings()

RESOURCE_DIR = os.getenv('RESOURCE_DIR', '/data/resources')
UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/data/uploads')

# Load shared env
try:
    _root_env = Path(__file__).resolve().parents[3] / '.env.shared'
    load_dotenv(str(_root_env), override=True)
except Exception:
    pass

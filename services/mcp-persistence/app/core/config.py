from pydantic import BaseModel
import os

class _Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/projects_db")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

settings = _Settings()

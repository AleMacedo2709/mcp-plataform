from celery import Celery
import os

def get_celery():
    broker = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    return Celery('mcp_ingestion_client', broker=broker, backend=backend)

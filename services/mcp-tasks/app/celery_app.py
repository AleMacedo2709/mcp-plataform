import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

app = Celery("mcp_tasks", broker=BROKER_URL, backend=BACKEND_URL)
app.conf.task_routes = {
    "tasks.normalize_file": {"queue": "ingestion"},
    "tasks.reindex_resources": {"queue": "ingestion"},
    "tasks.audit_webhook": {"queue": "audit"},
}

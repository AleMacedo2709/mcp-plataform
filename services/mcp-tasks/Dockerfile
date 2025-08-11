FROM ghcr.io/astral-sh/uv:python3.12-bookworm
WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --frozen --no-cache
COPY . .
RUN uv sync --frozen --no-cache
CMD ["uv", "run", "celery", "-A", "app.celery_app:app", "worker", "-l", "INFO", "-Q", "ingestion,audit"]

FROM ghcr.io/astral-sh/uv:python3.12-bookworm
WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --frozen --no-cache
COPY . .
RUN uv sync --frozen --no-cache
EXPOSE 8002
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

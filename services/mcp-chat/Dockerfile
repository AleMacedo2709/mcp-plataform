FROM ghcr.io/astral-sh/uv:python3.12-bookworm
WORKDIR /app
ENV PYTHONPATH=/app:/app/packages
COPY services/mcp-chat/pyproject.toml ./pyproject.toml
RUN uv sync --no-cache
COPY services/mcp-chat/ ./
COPY packages/ /app/packages/
RUN uv sync --no-cache
EXPOSE 8002
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

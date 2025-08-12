FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app
ENV PYTHONPATH=/app:/app/packages

# Copia manifest do serviço
COPY services/mcp-persistence/pyproject.toml ./pyproject.toml
RUN uv sync --no-cache

# Copia código do serviço e pacotes compartilhados
COPY services/mcp-persistence/ ./
COPY packages/ /app/packages/
RUN uv sync --no-cache

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

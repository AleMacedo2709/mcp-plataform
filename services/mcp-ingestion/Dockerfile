# Use imagem oficial do uv com Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app
ENV PYTHONPATH=/app:/app/packages

# Copia apenas manifestos primeiro (melhor cache)
COPY services/mcp-ingestion/pyproject.toml ./pyproject.toml
RUN uv sync --no-cache

# Copia restante do serviço e pacotes compartilhados
COPY services/mcp-ingestion/ ./
COPY packages/ /app/packages/

# Reinstala (caso haja extras) e prepara execução
RUN uv sync --no-cache

EXPOSE 8001

CMD ["uv", "run", "uvicorn", "mcp_ingestion.ingestion_server:app", "--host", "0.0.0.0", "--port", "8001"]

# Use imagem oficial do uv com Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

# Copia apenas manifestos primeiro (melhor cache)
COPY pyproject.toml ./

RUN uv sync --frozen --no-cache

# Copia restante do serviço
COPY . .

# Reinstala (caso haja extras) e prepara execução
RUN uv sync --frozen --no-cache

EXPOSE 8001

CMD ["uv", "run", "uvicorn", "mcp_ingestion.ingestion_server:app", "--host", "0.0.0.0", "--port", "8001"]

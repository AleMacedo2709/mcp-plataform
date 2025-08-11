# Variáveis de Ambiente
## Frontend
```
VITE_TEST_MODE=true
VITE_API_BASE_URL=http://localhost:8000
VITE_INGESTION_BASE_URL=http://localhost:8001
VITE_CHAT_BASE_URL=http://localhost:8002
VITE_AAD_CLIENT_ID=
VITE_AAD_TENANT_ID=
```

## mcp-persistence
```
ENVIRONMENT=local
ENV_FILE=.env.local
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/projects_db
CORS_ORIGINS=http://localhost:5173
USE_AUTH=false
AUDIT_WEBHOOK_URL=
OTEL_EXPORTER_OTLP_ENDPOINT=
```

## mcp-ingestion
```
ENVIRONMENT=local
ENV_FILE=.env.local
OPENAI_API_KEY=
OPENROUTER_API_KEY=changeme
LLM_MODEL=openrouter/anthropic/claude-3.5-sonnet
MAX_FILE_MB=50
RESOURCE_DIR=/data/resources
UPLOAD_DIR=/data/uploads
CNMP_CSV_SCHEMA=/app/mcp_ingestion/prompts/Formulario_CNMP_2025.csv
USE_AUTH=false
OTEL_EXPORTER_OTLP_ENDPOINT=
```

## mcp-chat
```
ENVIRONMENT=local
ENV_FILE=.env.local
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/projects_db
RESOURCE_DIR=/data/resources
OPENAI_API_KEY=
OPENROUTER_API_KEY=changeme
LLM_MODEL=openrouter/anthropic/claude-3.5-sonnet
CHAT_SUMMARIZE=true
EMB_MODEL=all-MiniLM-L6-v2
RAG_INDEX_DIR=/data/resources/.index
USE_AUTH=false
OTEL_EXPORTER_OTLP_ENDPOINT=
```

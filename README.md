# MCP Platform (Dev)

Monorepo com dois serviços Python prontos para rodar em desenvolvimento:

- **mcp-ingestion**: Upload + análise por IA (OpenRouter) dos documentos para extração dos 29 campos do formulário CNMP.
- **mcp-persistence**: API FastAPI de CRUD de Projetos + métricas de dashboard.

> **Observação:** Autenticação Azure AD e gateway serão adicionados depois. Este pacote funciona totalmente em modo DEV, dependendo apenas de variáveis `.env`.

## Requisitos
- Docker + Docker Compose
- (Opcional) Python 3.12 e [uv](https://github.com/astral-sh/uv) instalados localmente

## Subir com Docker Compose
```bash
docker compose up --build
```
Serviços expostos:
- API de Persistência: http://localhost:8000
- API de Ingestão/IA: http://localhost:8001
- Postgres: localhost:5432

## Variáveis de Ambiente
Copie e ajuste os `.env.example` de cada serviço para `.env`.

### mcp-ingestion
- `OPENROUTER_API_KEY`: chave do OpenRouter
- `LLM_MODEL`: ex.: `openrouter/anthropic/claude-3.5-sonnet`
- `ALLOW_DEMO`: `true|false` (em DEV pode ser `true`)
- `MAX_FILE_MB`: tamanho máximo do arquivo (padrão 50)

### mcp-persistence
- `DATABASE_URL`: ex.: `postgresql+psycopg2://postgres:postgres@db:5432/projects_db`
- `CORS_ORIGINS`: ex.: `http://localhost:5173,http://localhost:3000`

## Endpoints Principais
- **Ingestão/IA**
  - `POST /analyze` (multipart: `file`, query `analysis_type`) → `{ analysis: { ...29 campos... } }`
  - `GET /capabilities`
  - `GET /health`

- **Persistência**
  - `GET /projects` com filtros (`search`, `tipo_iniciativa`, `classificacao`, `fase`, `skip`, `limit`, `orderBy`, `order`)
  - `POST /projects`
  - `GET /projects/{id}`
  - `PUT /projects/{id}`
  - `DELETE /projects/{id}`
  - `GET /reports/dashboard`

> **Compatibilidade Frontend**: os endpoints e campos foram nomeados para casar com os componentes React enviados (ProjectList, ProjectForm, SmartProjectCreator, etc.).


## Frontend (apps/web-portal)
- Vite + React + MUI
- Rodar: `npm install && npm run dev` dentro de `apps/web-portal`


## Ambientes
Use docker compose com overrides:
```bash
# Local (padrão)
docker compose up --build

# Dev
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# UAT
docker compose -f docker-compose.yml -f docker-compose.uat.yml up --build

# Prod (simulado)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

Os serviços leem `ENVIRONMENT` e um `ENV_FILE` específico (ex.: `.env.uat`). Ajuste os `.env.*` em cada serviço.


## Observabilidade
- Logs em JSON por serviço
- `/metrics` Prometheus em cada serviço

## IA no Chat
- Para ativar a explicação por IA no chat, defina no `mcp-chat`:
  - `CHAT_SUMMARIZE=true` (padrão)
  - Forneça `OPENAI_API_KEY` ou `OPENROUTER_API_KEY`

## AAD/MSAL (placeholders)
- Frontend (`apps/web-portal/.env`): `VITE_AAD_CLIENT_ID`, `VITE_AAD_TENANT_ID`
- Backend: `USE_AUTH=true` e variáveis esperadas por `auth/entra.py`.


## Observability++ (Prometheus + Grafana + Traces)
- Subir stack de observabilidade:
```bash
docker compose -f docker-compose.yml -f docker-compose.observability.yml up -d otel-collector tempo prometheus grafana
```
- Configure nas APIs: `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`
- Acesse Grafana: http://localhost:3000 (admin/admin)
  - Prometheus em `http://prometheus:9090`
  - Tempo em `http://tempo:3200`

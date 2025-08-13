## Entrega para TI — Guia de Implantação e Operação

Este documento resume como o sistema está estruturado, como construir e operar em DEV/UAT/PROD, e as variáveis essenciais. Foi escrito para equipes de TI que vão manter e publicar o sistema.

### Arquitetura de alto nível

- **Frontend (Vite/React)**: `apps/web-portal` — UI do portal (Chat, Nova Iniciativa, Edição, Listagem)
- **Persistência (FastAPI)**: `services/mcp-persistence` — CRUD de iniciativas, membros, contatos, resultados, prêmios, anexos
- **Ingestão (FastAPI + IA)**: `services/mcp-ingestion` — Upload/análise de documentos, extração estruturada com LLM
- **Chat (FastAPI + WebSocket)**: `services/mcp-chat` — Chat de busca/explicação com RAG e WS
- **Infra**: PostgreSQL, Redis, ClamAV (antivírus) — orquestrados via `docker-compose.yml`

Portas padrão (localhost):
- Persistência: 18000 (HTTP)
- Ingestão: 18001 (HTTP)
- Chat: 18002 (HTTP/WS)
- Frontend: 5173 (HTTP)
- ClamAV: 3310 (TCP)

### Como subir localmente

1) Pré-requisitos: Docker/Docker Compose, porta 5173 livre
2) Subir stack:
```
docker compose up -d
```
3) Acessar o portal: `http://localhost:5173`

Comandos úteis:
```
# rebuild apenas do frontend
docker compose up -d --no-deps --build web-portal

# health checks
curl http://localhost:18000/health
curl http://localhost:18001/health
curl http://localhost:18002/health
```

### Perfis de documentação (MkDocs)

- Dev/local: `mkdocs serve -f infra/config/mkdocs-dev.yml`
- UAT: `mkdocs build -f infra/config/mkdocs-uat.yml -d site-uat`
- Prod: `mkdocs build -f infra/config/mkdocs-prod.yml -d site`

`mkdocs.yml` na raiz herda `infra/config/mkdocs-base.yml` e pode ser usado como default simples.

### Variáveis de ambiente (chaves principais)

Definidas em `docker-compose.yml` e `.env.shared` (se existir). Ajuste para o ambiente alvo.

- Frontend (`web-portal`)
  - `VITE_API_BASE_URL` → URL do serviço de persistência
  - `VITE_INGESTION_BASE_URL` → URL do serviço de ingestão
  - `VITE_CHAT_BASE_URL` → URL do serviço de chat

- Persistência (`mcp-persistence`)
  - `DATABASE_URL` (via settings) — use Postgres gerenciado em PROD
  - `AUTO_MIGRATE=true` — aplica migrações automaticamente (recomendado apenas na primeira subida)
  - `CORS_ORIGINS` — domínios autorizados
  - `USE_AUTH=true` — exige autenticação em PROD
  - `CLAMAV_HOST=clamav`, `CLAMAV_PORT=3310`

- Ingestão (`mcp-ingestion`)
  - `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` — Redis
  - `LLM_PROVIDER` — `azure` | `openai` | `openrouter` | `demo`
  - `ALLOW_DEMO=false` (use `true` apenas em demonstrações)
  - Credenciais do provedor conforme `LLM_PROVIDER` (AZURE_OPENAI_*, OPENAI_*, OPENROUTER_*)
  - `CORS_ORIGINS`, `USE_AUTH=true`

- Chat (`mcp-chat`)
  - `USE_AUTH=true` (WS exige token via header ou query `?token=`)
  - `CORS_ORIGINS`

### Segurança (produção)

- Definir `CORS_ORIGINS` para os domínios oficiais (portal e APIs)
- Ativar `USE_AUTH=true` (serviços rejeitam acesso anônimo em PROD)
- Antivírus: manter `clamav` saudável; uploads são escaneados
- Rate limiting: já configurado (SlowAPI) em serviços e rotas sensíveis
- CSP/Ingress/Nginx: restringir `connect-src` aos backends publicados
- Segredos: usar cofre de segredos (KeyVault/Secrets Manager)

### Autenticação e tokens (frontend)

- `apps/web-portal/src/hooks/useAuth.js` integra MSAL e expõe `user.token`
- Token é enviado em chamadas HTTP/WS quando disponível
- Em UAT/DEV é possível operar sem token conforme flags atuais (ajustar para o ambiente)

### Fluxo “Nova Iniciativa” e IA

1) Upload de documento → Ingestão → IA extrai campos estruturados
2) “Criação Inteligente” e “Nova Iniciativa” pré-preenchem:
   - 29 campos base & campos estruturados adicionais (equipe, contatos, comprovações, prêmios)
3) Ao salvar/criar, as listas dinâmicas são enviadas automaticamente:
   - `POST /projects/{id}/members`
   - `POST /projects/{id}/contacts`
   - `POST /projects/{id}/results`
   - `POST /projects/{id}/awards`

Componentes reutilizáveis no frontend:
- `TeamFields.jsx`, `ContactsFields.jsx`, `ResultsFields.jsx` — usados por `ProjectForm` e `SmartProjectCreator`

### Padrões de código e qualidade

- Frontend: React + MUI; variáveis padronizadas `VITE_*`; componentes extraídos para evitar duplicidade
- Backend: FastAPI estruturado por domínio; rotas com limitações de taxa; uploads validados; ClamAV
- Logs/observabilidade: endpoints `/health` e `/metrics` (protegido por role `admin` em PROD)

### Troubleshooting

- Frontend não atualiza UI após ajuste: rebuild do serviço `web-portal` e hard refresh no navegador
- Erro 18001/analyze: verifique se `mcp-ingestion` está up e `slowapi` instalado (já em `pyproject.toml`)
- WebSocket fechado: subir `mcp-chat` e conferir flag `USE_AUTH`

### Roadmap recomendado para TI (opcional)

- CI/CD: pipeline para `docker build` e `mkdocs build`
- Linters: ESLint/Prettier (frontend) e Ruff/Flake8 (Python)
- Telemetria: coletar métricas e logs centralizados



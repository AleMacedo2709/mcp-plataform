# MCP Platform — Guia Rápido

Este repositório contém o portal web, serviços FastAPI (persistência/ingestão/chat) e documentação MkDocs.

## Documentação (MkDocs)

- Dev/local: `mkdocs serve -f infra/config/mkdocs-dev.yml`
- UAT: `mkdocs build -f infra/config/mkdocs-uat.yml -d site-uat`
- Prod: `mkdocs build -f infra/config/mkdocs-prod.yml -d site`

Página de entrega para TI: consulte `docs/operacao/entrega-ti.md` (também no menu Operação).

## Subir localmente (Docker)

```bash
docker compose up -d
# Rebuild somente do frontend
docker compose up -d --no-deps --build web-portal
```

Portas padrão: 5173 (web), 18000 (persistência), 18001 (ingestão), 18002 (chat), 3310 (ClamAV).

Health checks:

```bash
curl http://localhost:18000/health
curl http://localhost:18001/health
curl http://localhost:18002/health
```

## Variáveis de ambiente principais

- Frontend: `VITE_API_BASE_URL`, `VITE_INGESTION_BASE_URL`, `VITE_CHAT_BASE_URL`
- Serviços: `CORS_ORIGINS`, `USE_AUTH`, `CLAMAV_HOST/PORT`, chaves LLM conforme provedor

Para mais detalhes, veja a página "Entrega para TI" e os arquivos de `infra/config/`.



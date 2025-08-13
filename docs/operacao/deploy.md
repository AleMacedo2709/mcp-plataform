# Operação & Deploy
## Ambientes
Use os `docker-compose.*.yml` para subir **dev/uat/prod** com overrides.

## Migrações
- DEV/LOCAL: opcionalmente via `AUTO_MIGRATE=true` (padrão: desligado).
- UAT/PROD: executar manualmente `alembic upgrade head` dentro do container `mcp-persistence`.

## Auditoria
- Configure `AUDIT_WEBHOOK_URL` para receber notificações de criação/edição/remoção de projetos.

## Produção
- Backend: o compose-prod usa `gunicorn` com `uvicorn` (4 workers). Ajuste CPU/RAM conforme carga.
- Frontend: gerar build (`npm run build`) e servir com CDN/Nginx (compose-prod usa `serve` como referência).
- Segurança: `USE_AUTH=true`, `INCLUDE_INSTITUTIONAL_ROUTES=false`, CORS restrito ao domínio do frontend.
- Saúde: `GET /health` e `GET /readiness` para probes.

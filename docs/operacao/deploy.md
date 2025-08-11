# Operação & Deploy
## Ambientes
Use os `docker-compose.*.yml` para subir **dev/uat/prod** com overrides.

## Migrações
- DEV/LOCAL: aplicadas automaticamente no startup.
- UAT/PROD: executar manualmente `alembic upgrade head` (em `mcp-persistence`).

## Auditoria
- Configure `AUDIT_WEBHOOK_URL` para receber notificações de criação/edição/remoção de projetos.

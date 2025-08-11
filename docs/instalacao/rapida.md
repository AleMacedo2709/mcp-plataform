# Guia Rápido (DEV)
1. **Subir serviços**:
```bash
docker compose up --build
```
2. (Opcional) **Observabilidade**:
```bash
docker compose -f docker-compose.yml -f docker-compose.observability.yml up -d otel-collector tempo prometheus grafana
```
3. Acessos:
- Front: http://localhost:5173
- Persistência: http://localhost:8000
- Ingestão: http://localhost:8001
- Chat: http://localhost:8002

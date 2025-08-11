# Observabilidade
- **Logs JSON** (um por serviço).
- **/metrics** Prometheus (latência, contadores).
- **OpenTelemetry** (traces) exportados via OTLP para o Collector.
- Dashboards em **Grafana** (Prometheus + Tempo).

## Subindo a stack
```bash
docker compose -f docker-compose.yml -f docker-compose.observability.yml up -d otel-collector tempo prometheus grafana
```
Depois, configure `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318` nas APIs.

# Plataforma de Submissão e Gestão de Projetos (MP)
Bem-vindo à documentação oficial da plataforma.

## Objetivo
O sistema otimiza a **submissão** e **gestão** de projetos com:
- Arquitetura **microsserviços**, **conteneirizada**.
- **IA** para pré-preenchimento de 29 campos do formulário **Prêmio CNMP**.
- Autenticação **Azure AD** (a configurar pela TI).
- Segurança, observabilidade e RAG persistente.

## Componentes
- **Frontend (apps/web-portal)** — React (Vite + MUI).
- **mcp-persistence** — FastAPI (CRUD de projetos + relatórios).
- **mcp-ingestion** — FastAPI (upload, parsing, IA de extração e normalização para RAG).
- **mcp-chat** — FastAPI + MCP SDK (busca por projetos/resources e respostas com IA).
- **Postgres** — armazenando projetos.
- **Observabilidade** — Prometheus, Grafana, OTel Collector, Tempo.

> Esta doc segue o padrão institucional e está pronta para publicação via MkDocs.

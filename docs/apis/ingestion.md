# API — Ingestão
Base: `http://localhost:8001`

- `POST /analyze?analysis_type=analyze_project_document_cnmp` (multipart: `file`)
- `GET /health`

> Normalização: cada documento processado gera uma cópia `.txt` em `RESOURCE_DIR`.

# Microsserviços
## mcp-persistence
- FastAPI + SQLAlchemy 2.0
- Alembic (migração auto em `local/dev`)
- RBAC básico (headers em dev; AAD via `USE_AUTH=true`)

## mcp-ingestion
- Upload (checagem de tamanho + 413)
- Parsing (PDF/DOCX) e normalização para `.txt`
- IA unificada (OpenAI/OpenRouter) com validação dinâmica via CSV dos 29 campos

## mcp-chat
- MCP SDK oficial (ferramentas: query_project, get_project_by_id, search_resources, faq_campos_cnmp)
- HTTP `/ask` + WebSocket `/ws`
- RAG persistente (SQLite + `.npy`) com **Embeddings + BM25 (híbrido)** e fallback TF-IDF

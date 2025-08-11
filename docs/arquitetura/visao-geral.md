# Arquitetura — Visão Geral
A solução adota arquitetura **microsserviços** separando responsabilidades:
- **Persistência**: CRUD + relatórios.
- **Ingestão/IA**: upload, parsing, extração e normalização de documentos em `RESOURCE_DIR`.
- **Chat (MCP)**: camadas de busca (DB + RAG) + explicação via IA unificada.
- **Frontend**: SPA em React.

## Diagrama Lógico (alto nível)
```
[Web (React)] <-> [mcp-persistence] <-> [Postgres]
        |                 |
        v                 |
    [mcp-ingestion] ------+
        |
       RAG (resources) <-> [mcp-chat] (MCP SDK, Embeddings+BM25, TF-IDF)
```

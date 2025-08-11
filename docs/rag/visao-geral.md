# RAG — Visão Geral
- **Normalização**: PDFs/DOCX geram `.txt` no `RESOURCE_DIR` durante a ingestão.
- **Index persistente**: SQLite + vetores `.npy` em `/data/resources/.index`.
- **Busca híbrida**: **Embeddings** (`all-MiniLM-L6-v2`) + **BM25**, com fallback para TF-IDF.
- **Highlights**: termos em negrito nos trechos retornados.

## Atualização do índice
O índice é incremental por arquivo (mtime + hash). Ao substituir um documento, ele é reprocessado.

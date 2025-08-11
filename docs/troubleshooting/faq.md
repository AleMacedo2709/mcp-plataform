# Troubleshooting
**Erro 413 no upload** — arquivo excede `MAX_FILE_MB` (ajuste no `.env`).  
**Sem explicação por IA** — configure `OPENAI_API_KEY` ou `OPENROUTER_API_KEY`.  
**/metrics vazio** — confirme Prometheus coletando e middleware habilitado.  
**Sem documentos no RAG** — verifique se `.txt` normalizado está sendo gravado em `RESOURCE_DIR`.

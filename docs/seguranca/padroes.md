# Segurança — Padrões Adotados
- **CSP/COOP/CORP** configurados via middleware.
- **X-Frame-Options: DENY**, **X-Content-Type-Options: nosniff**, **Referrer-Policy: no-referrer**.
- **Limites de upload** (tamanho checado no servidor).
- **RBAC** básico por rotas (dev por header; produção via AAD).
- **Auditoria**: webhook em eventos de CRUD.

> Em produção, usar **Key Vault** (ou equivalente) para segredos e rotacionar chaves.

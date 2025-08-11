# API — Chat
Base: `http://localhost:8002`

- `POST /ask` → `{ answer, results|hits|data, explanation? }`
- `WS /ws` → envia `{ question }`, recebe `{ type: "answer", payload }`

Ferramentas **MCP** internas para integrações avançadas:
- `query_project(term, limit)`
- `get_project_by_id(project_id)`
- `search_resources(query, limit)`
- `faq_campos_cnmp(nome_campo)`

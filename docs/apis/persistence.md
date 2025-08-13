# API — Persistência
Base (dev): `http://localhost:18000`
Base (prod): `${VITE_API_BASE_URL}`

## Projetos
- `GET /projects?search=&skip=&limit=&tipo_iniciativa=&classificacao=&fase=&orderBy=&order=`
- `POST /projects`
- `GET /projects/{id}`
- `PUT /projects/{id}`
- `DELETE /projects/{id}`
  - Permissões: admin, owner do projeto ou membro da equipe

## Relatórios
- `GET /reports/dashboard`

## Uploads
- `POST /projects/{id}/attachments` — Anexos (50MB máx; tipos: pdf/png/jpg/jpeg/docx/txt; validação MIME)
- `GET /projects/{id}/attachments` — Lista anexos
- `GET /projects/{id}/attachments/{attachment_id}/download` — Download direto
- `POST /projects/{id}/cover` — Capa (10MB máx; png/jpg/jpeg; validação MIME)
- `GET /projects/{id}/cover` — Última capa

## Equipe
- `GET /projects/{id}/members`
- `POST /projects/{id}/members` — body: `{name, email, role}`
- `PUT /projects/{id}/members/{member_id}` — body parcial `{name?, email?, role?}`
- `DELETE /projects/{id}/members/{member_id}`

## Saúde do serviço
- `GET /health` — liveness
- `GET /readiness` — verifica conexão com DB

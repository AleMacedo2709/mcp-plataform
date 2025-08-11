# Web Portal (React + Vite)

## Rodar localmente
```bash
npm install
npm run dev
```
- URL: http://localhost:5173

## Configuração
Edite `.env` (já criado a partir do `.env.example`):

```
VITE_TEST_MODE=true
VITE_API_BASE_URL=http://localhost:8000
VITE_INGESTION_BASE_URL=http://localhost:8001
```

> Quando ativarmos Azure AD, preencha `VITE_AAD_CLIENT_ID` e `VITE_AAD_TENANT_ID`.


## MSAL / AAD
Preencha `.env` com:
```
VITE_AAD_CLIENT_ID=<clientId>
VITE_AAD_TENANT_ID=<tenantId>
```
No backend, configure `USE_AUTH=true` e variáveis esperadas pelo middleware `entra`.

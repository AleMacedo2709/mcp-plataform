# Arquivo de Configuração

As variáveis de ambiente da aplicação estão contidas em um arquivo `.env`. Foram definidos arquivos distintos para cada ambiente:

| Ambiente     | Arquivo               |
| ------------ | --------------------- |
| `.env.local` | Desenvolvimento Local |
| `.env.dev`   | Desenvolvimento MPSP  |
| `.env.uat`   | Homologação MPSP      |
| `.env.prod`  | Produção MPSP         |

<br>

As variáveis contidas no `.env*` são listadas abaixo. Ainda, a definição de qual arquivo `.env*` usar está definido na variável `AMBIENTE`, definida em:

```shell
nano /ania/config.py
```

<br>

```shell
# Aplicação
APP_SECRET_KEY=************

# Database Aplicação
POSTGRES_HOST=mpdbtilene
POSTGRES_PORT=5432
POSTGRES_DATABASE=ania
POSTGRES_USERNAME=ania_user
POSTGRES_PASSWORD=************

# Database Logs
POSTGRES_HOST_LOGS=mpdbtilene
POSTGRES_PORT_LOGS=5432
POSTGRES_DATABASE_LOGS=ania_logs
POSTGRES_USERNAME_LOGS=ania_user
POSTGRES_PASSWORD_LOGS=************

# Redis/Celery
REDIS_CONN_STRING=redis://localhost:6379/0

# Azure - Microsoft Entra ID
# A variável AZURE_TENANT_ID também é usada para configuração da autenticação
AZURE_TENANT_ID=2db************

# Azure - Microsoft OpenAI
OPENAI_API_KEY=1iY************
OPENAI_API_TYPE=azure
OPENAI_API_VERSION=2023-05-15
OPENAI_API_BASE=https://openai******.azure.com/
OPENAI_MODEL=gpt-4o

# Azure - App Registration - Login
# ANIA-TILENE-Testes
AUTH_CLIENT_ID=5f7************
AUTH_CLIENT_SECRET=_MA************
AUTH_REDIRECT_URI=https://tilene************/getAToken
AUTH_ENDPOINT=https://graph.microsoft.com/v1.0/me
AUTH_SCOPE=User.Read

# Flask Session
SESSION_TYPE=filesystem

# Logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=DEBUG
# LOGS_FILEPATH=/var/log/tilene_app.log
```

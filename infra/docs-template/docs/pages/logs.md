# Monitoramento

Estou fazendo o monitoramento da aplicação _gunicorn_ (em dev a partir de 05.06.2025)

```shell
# Celery
cat /var/log/tilene_celery.log

# Flower
cat /var/log/tilene_flower.log

# Gunicorn-Flask
cat /var/log/tilene_gunicorn_access.log
cat /var/log/tilene_gunicorn_error.log

# Aplicação
cat /var/log/tilene_app.log
```

<br>

---

## Utilização

_Log_ de uso para verificação do consumo da IA.

```sql
SELECT id, id_usuario, arquivo, api, total_tokens, data
FROM public.log_uso_api
ORDER BY data desc;
```

<br>

---

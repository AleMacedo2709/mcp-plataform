# Como Rodar?

Abaixo são apresentadas informações para rodar localmente.

## Celery

No diretório do projeto executar:

- [Celery Execution Pools: What is it all about?](https://celery.school/celery-worker-pools)

```shell
# Padrão (que estou usando)
celery --app ania.celery_worker worker --loglevel info

# Opcional
# Usado pelo TCE
celery --app ania.celery_worker worker --loglevel info --pool=eventlet

# Celery para Versão 2.0.0 sem autenticação (ANIA)
celery --app app_noauth.celery worker --loglevel info --pool=solo

# Padrão (que estou usando)
celery --app ania.main_app worker --loglevel info --pool=eventlet # Erro
celery --app ania.main_app worker --loglevel info
celery --app ania.main_app worker --loglevel DEBUG --logfile ./tools/data/logs/tilene_celery.log --pool=gevent --concurrency=200
```

<br>

---

## Flower

O [Flower](https://flower.readthedocs.io/en/latest/) ([GitHub](https://github.com/mher/flower)) fornece uma interface para monitorar as _tasks_.

```shell
# Celery com Flower
celery --app ania.celery_worker flower --loglevel=INFO --port=5555

# Celery com Flower e senha
celery --app ania.celery_worker flower --loglevel=INFO --port=5555 --basic-auth=michelsilva:subinova

# Celery com Flower
celery --app ania.main_app flower --loglevel=DEBUG --logfile ./tools/data/logs/tilene_flower.log --port=5555 --url_prefix=flower
```

<br>

---

## _Flask_

Deixei a aplicação principal no arquivo `main_app.py` e dessa forma eu posso chamar a aplicação por meio do comando `ania.main_app`.

```shell
# Roda
flask --app ania.main_app run --host 0.0.0.0 --port 5000

# Com debug (estou usando)
flask --app ania.main_app run --host 0.0.0.0 --port 5000 --debug

# ANIA
flask --app app_noauth run --host=0.0.0.0 --port=5000

# Com debug (estou usando a partir de 14.04.2025)
flask --app ania run --host 0.0.0.0 --port 5000 --debug
```

<br>

Deverá abrir uma aba no seu navegador padrão. Em caso negativo, o serviço deverá ester disponível em:

> http://127.0.0.1:5000

<br>

---

## _Flask_ via Gunicorn

Apenas para fins de teste, avaliamos se o `gunicorn` consegue servir a aplicação.

```shell
# Gunicorn com bind no endereço
gunicorn --bind 0.0.0.0:5000 "ania:create_app()"

# Gunicorn com bind no endereço localhost
# Não deu certo no Nitro, WSL, Ubuntu 24.04 em 06.05.2025
# Deu certo no Nitro, WSL, Ubuntu 24.04 em 06.05.2025
gunicorn --bind 127.0.0.1:5000 "ania:create_app()"

# Gunicorn com socks
gunicorn --bind unix:ania.sock "ania:create_app()"

# Mata qualquer coisa na porta 5000
sudo kill -9 $(sudo lsof -t -i:5000)
```

<br>

---

## MkDocs / Documentação

A documentação da aplicação foi feita usando o [MkDocs](https://www.mkdocs.org/).

```shell
# Serve a documentação em localhost, porta 8000
mkdocs serve

# Serve arquivo específico
mkdocs serve --config-file mkdocs-dev.yml
mkdocs serve --config-file mkdocs-uat.yml
mkdocs serve --config-file mkdocs-prod.yml
```

<br>

???+ warning "Atenção"

    Lembrar de editar qual será a documentação que será "servida":<br>
    - dev<br>
    - uat<br>
    - prod

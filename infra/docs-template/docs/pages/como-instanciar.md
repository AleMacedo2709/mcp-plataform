# Como Instanciar?

## Código

**Passo 1**: Crie um usuário para a aplicação. Sugestão de criar um usuário chamado `tilene`, e criar uma pasta onde a aplicação ficará "hopesdada".

```shell
# Adiciona Usuário
sudo adduser tilene

# Cria pasta
sudo mkdir -p /opt/tilene

# Dá permissões à pasta, para o usuário
sudo chown tilene:tilene /opt/tilene

# Vai pra pasta
cd /opt/tilene

# Vai pro usuário root
sudo su

# A partir do root, entra no usuário tilene
su - tilene
```

**Passo 2**: Uma vez na pasta `tilene`, com o usuário `tilene`, extraia o projeto. Para obter o código do _repo_ [CGE/ANIA_TCE_Core](https://dev.azure.com/mpsp/CGE/_git/ANIA_TCE_Core), é necessário fazer o `git clone` (ver mais em [código](código.md)). Recomenda-se o clone do código na pasta `/opt`...

```shell
# Git (será necessário as devidas pemissões e senhas)
git clone https://mpsp@dev.azure.com/mpsp/CGE/_git/ANIA_TCE_Core

# Vai pra pasta
cd /opt/tilene/ANIA_TCE_Core
```

???+ note

    É necessário que a estrutura de pastas se assemelhe ao demostrado abaixo:
    ```shell
    /opt
    └── tilene
        └── ANIA_TCE_Core
            ├── ania
            ├── docs
            ├── scripts
            └── tools
    ```

**Passo 3**: Criar ambiente do _python_ (ver mais em [python](python.md))

<br>

---

## Requisitos

**Passo 1**: Instalar o PostGreSQL (ver mais em [Database](database.md))<br>
**Passo 2**: Instalar o pgVector (ver mais em [Database#pgVector](database.md#extensao_pgvector))<br>
**Passo 3**: Instalar o Redis (ver mais em [Redis e Celery](redis-e-celery.md))<br>
**Passo 4**: Crias _dbs_, usuário dos _dbs_ (e ajustar permissões) e tabelas (ver mais em [Estrutura dos Dados](dados.md))<br>

<br>

---

## Configurações

**Passo 1**: Ajustar as variáveis de ambiente contidas em um dos arquivos, a depender de qual ambiente se está utilizando:

- `.env.local`: para ambiente local
- `.env.dev`: para ambiente de desenvolvimento
- `.env.uat`: para ambiente de homologação
- `.env.prod`: para ambiente de produção

Talvez seja necessário criar/configurar o arquivo contendo as variáveis de ambientes e/ou _secrets_.

```shell
# Cria arquivo
nano .env.local
nano .env.dev
nano .env.uat
nano .env.prod
```

**Passo 2**: No arquivo `ania/config.py` é necessário ajustar a variável `AMBIENTE` para uma opção do ambiente se se deseja fazer _deploy_.

```shell
# Edita a variável do código
nano /opt/tilene/ANIA_TCE_Core/ania/config.py
```

???+ note

    Isso será ajustado no futuro. Ideia de ler o nome do servidor de aplicação, definindo automaticamente o conjunto de _.envs_ que irá consumir.

<br>

---

## Serviços

Optou-se por instanciar a aplicação via _serviços_ (`systemd`). Para que a aplicaço rode, são necessários alguns serviços:

### Celery

Necessário para que a tarefa de _upload_ de arquivos funcione sem travar a aplicação. Ver mais em [Redis e Celery](redis-e-celery.md).

```shell
# Cria o arquivo diretamente
sudo tee /etc/systemd/system/tilene_celery.service > /dev/null << EOF
[Unit]
Description=Celery instance to serve Tilene
After=network.target

[Service]
WorkingDirectory=/opt/tilene/ANIA_TCE_Core/
Environment="PATH=/opt/tilene/ANIA_TCE_Core/.venv/bin"
ExecStart=/opt/tilene/ANIA_TCE_Core/.venv/bin/celery \
        --app ania.main_app worker \
        --loglevel DEBUG \
        --logfile /var/log/tilene_celery.log \
        --pool=gevent \
        --concurrency=200

[Install]
WantedBy=multi-user.target
EOF
```

<br>

```shell
# Vê conteúdo
cat /etc/systemd/system/tilene_celery.service

# Excluí serviço
sudo rm /etc/systemd/system/tilene_celery.service
```

<br>

Agora ele pode ser iniciado etc....

```shell
# Reload após criar/modificar
sudo systemctl daemon-reload

# Start/Stop
sudo systemctl start tilene_celery.service
sudo systemctl stop tilene_celery.service
sudo systemctl restart tilene_celery.service
sudo systemctl status tilene_celery.service
```

<br>

```shell
# Habilitar/Desabilitar no boot
sudo systemctl enable tilene_celery.service
sudo systemctl disable tilene_celery.service
```

<br>

---

### _Flower_

O [Flower](https://flower.readthedocs.io/en/latest/) ([GitHub](https://github.com/mher/flower)) fornece uma interface para monitorar as _tasks_ do (#celery).

```shell
# Cria o arquivo diretamente
sudo tee /etc/systemd/system/tilene_flower.service > /dev/null << EOF
[Unit]
Description=Celery instance to serve Tilene
After=network.target
After=tilene_celery.service

[Service]
WorkingDirectory=/opt/tilene/ANIA_TCE_Core/
Environment="PATH=/opt/tilene/ANIA_TCE_Core/.venv/bin"
ExecStart=/opt/tilene/ANIA_TCE_Core/.venv/bin/celery \
        --app ania.main_app flower \
        --loglevel=DEBUG \
        --logfile /var/log/tilene_flower.log \
        --address='0.0.0.0' \
        --basic-auth=michelsilva:flowerpower \
        --url_prefix=flower \
        --port=5555

[Install]
WantedBy=multi-user.target
EOF
```

<br>

```shell
# Vê conteúdo
cat /etc/systemd/system/tilene_flower.service

# Excluí serviço
sudo rm /etc/systemd/system/tilene_flower.service
```

<br>

Agora ele pode ser iniciado etc....

```shell
# Reload após criar/modificar
sudo systemctl daemon-reload

# Start/Stop
sudo systemctl start tilene_flower.service
sudo systemctl stop tilene_flower.service
sudo systemctl restart tilene_flower.service
sudo systemctl status tilene_flower.service
```

<br>

```shell
# Habilitar/Desabilitar no boot
sudo systemctl enable tilene_flower.service
sudo systemctl disable tilene_flower.service
```

<br>

---

### _Flask_ via Gunicorn

Cria um serviço para server a aplicação, com auxílio do [_gunicorn_](https://gunicorn.org/).

```shell
# Cria o arquivo diretamente
sudo tee /etc/systemd/system/tilene_flask.service > /dev/null << EOF
[Unit]
Description=Gunicorn instance to serve Tilene
After=network.target
After=tilene_celery.service
After=tilene_flower.service

[Service]
WorkingDirectory=/opt/tilene/ANIA_TCE_Core/
Environment="PATH=/opt/tilene/ANIA_TCE_Core/.venv/bin"
ExecStart=/opt/tilene/ANIA_TCE_Core/.venv/bin/gunicorn \
    --workers 8 \
    --bind 127.0.0.1:5000 \
    --access-logfile /var/log/tilene_gunicorn_access.log \
    --error-logfile /var/log/tilene_gunicorn_error.log \
    --log-level DEBUG \
    -m 007 "ania:create_app()"

[Install]
WantedBy=multi-user.target
EOF
```

<br>

```shell
# Vê conteúdo
cat /etc/systemd/system/tilene_flask.service

# Excluí serviço
sudo rm /etc/systemd/system/tilene_flask.service
```

<br>

Agora ele pode ser iniciado etc....

```shell
# Reload após criar/modificar
sudo systemctl daemon-reload

# Start/Stop
sudo systemctl start tilene_flask.service
sudo systemctl stop tilene_flask.service
sudo systemctl restart tilene_flask.service
sudo systemctl status tilene_flask.service
```

<br>

```shell
# Habilitar/Desabilitar no boot
sudo systemctl enable tilene_flask.service
sudo systemctl disable tilene_flask.service
```

<br>

---

### MkDocs / Documentação

Na implantação do sistema no TCE-SP existe uma FAQ implantada no _Sharepoint_. Como não temos essa FAQ, optou-se por criar uma documentação.

Ainda, para ajusta ro caminho, foi necessário alterar uma linha do `index.html` (caminho `./app/templates`). Esta linha é exemplificada no código como:

```html
<a href="https://url_orgao.sharepoint.com/sites/ANIA/SitePages/Ajuda-e-Suporte.aspx" class="nav-link text-dark text-truncate" target="_blank"> Ajuda e Suporte </a>
```

<br>

O _post_ [Create a Systemd service in Ubuntu to run MKDocs](https://askubuntu.com/questions/1390667/create-a-systemd-service-in-ubuntu-to-run-mkdocs) trata da documentação como serviço. Para criar o serviço basta usar o comando abaixo.

```shell
# Serve a documentação em localhost, porta 8000
sudo tee /etc/systemd/system/tilene_mkdocs.service > /dev/null << EOF
[Unit]
Description=MkDocs instance to serve Tilene's docs
After=network.target

[Service]
WorkingDirectory=/opt/tilene/ANIA_TCE_Core/
Environment="PATH=/opt/tilene/ANIA_TCE_Core/.venv/bin"
ExecStart=/opt/tilene/ANIA_TCE_Core/.venv/bin/mkdocs serve --config-file mkdocs-dev.yml

[Install]
WantedBy=multi-user.target
EOF
```

<br>

```shell
# Vê conteúdo
cat /etc/systemd/system/tilene_mkdocs.service

# Excluí serviço
sudo rm /etc/systemd/system/tilene_mkdocs.service
```

<br>

Agora ele pode ser iniciado etc....

```shell
# Reload após criar/modificar
sudo systemctl daemon-reload

# Start/Stop
sudo systemctl start tilene_mkdocs.service
sudo systemctl stop tilene_mkdocs.service
sudo systemctl restart tilene_mkdocs.service
sudo systemctl status tilene_mkdocs.service
```

<br>

```shell
# Habilitar/Desabilitar no boot
sudo systemctl enable tilene_mkdocs.service
sudo systemctl disable tilene_mkdocs.service
```

<br>

---

## Apache

Para expor a aplicação "para fora", foi utilizado configuração de _proxy reverso_ do Apache.

```shell
# Cria o arquivo diretamente
sudo tee /etc/httpd/conf.d/tilene_webserver.conf > /dev/null << EOF
<Location />
    Require all granted
    ProxyPass http://localhost:5000/
    ProxyPassReverse http://localhost:5000/
    SSLRequireSSL On
</Location>

<Location /docs/>
    Require all granted
    ProxyPass http://localhost:8000/docs/
    ProxyPassReverse http://localhost:8000/docs/
    SSLRequireSSL On
</Location>

<Location /flower/>
    Require all granted
    ProxyPass http://localhost:5555/flower/
    ProxyPassReverse http://localhost:5555/flower/
    SSLRequireSSL On
</Location>
EOF
```

<br>

```shell
# Vê conteúdo
cat /etc/httpd/conf.d/tilene_webserver.conf

# Excluí host
sudo rm /etc/httpd/conf.d/tilene_webserver.conf
```

<br>

Para ver as configurações existentes

```shell
# Lista Configurações
cd /etc/httpd/conf.d/ && ls -la
```

<br>

```shell
# Reinicia Apache
sudo systemctl restart httpd

# Start/Stop etc
sudo systemctl restart httpd
sudo systemctl stop httpd
sudo systemctl start httpd
sudo systemctl reload httpd
sudo systemctl status httpd
```

<br>

???+ note

    Idéia futura de testar abrir outros _locations_ no _Apache_.

    - Usar `tilenedev.mpsp.mp.br` para a aplicação.<br>
    - Usar `tilenedev.mpsp.mp.br/flower/` para o _flower_.<br>
    - Usar `tilenedev.mpsp.mp.br/docs/` para a documentação.<br>

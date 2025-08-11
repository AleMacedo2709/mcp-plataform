# _Database_

O ANIA-TCE usar o **PostgreSQL**. Foram testadas as versões 14 e 15 pelo TCE. Recomenda-se a instalação do _PostgreSQL_ em uma máquina Linux, visando facilitar a instalação da extensão necessária.

É importante ressaltar que o banco de dados denominado `ania` foi criado com:

- _Encoding_ UTF8
- _Collation_ e _character type_: pt_BR.UTF-8
- Também funciona com _collation_ e _character type_ POSIX.

???+ note "Nota"

    De acordo com o TCE, a razão de instalar o _PostgreSQL_ em máquinas Linux é devido ao fato de que a extensão _pgvector_ para sistemas instalados em _Windows_ não funcionaram adequadamente quando foi testado em 2023.

<br>

---

## Instalando o _db_

### No Ubuntu (Debian _based_)

Para instalar o [PostgreSQL](https://www.postgresql.org/).

```shell
# Atualiza pacotes
sudo apt update -y && sudo apt upgrade -y

# Adiciona Chaves
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg

# Adiciona Repos
echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# Instala
sudo apt update -y && sudo apt install postgresql-15 -y
```

<br>

Para ver os serviços.

```shell
# Status
sudo systemctl status postgresql

# Start
sudo systemctl start postgresql

# Restart
sudo systemctl restart postgresql

# Enable
sudo systemctl enable postgresql
```

<br>

Apenas para validar a porta que está sendo usada...

```shell
# Instala
sudo apt install net-tools -y

# Confere
netstat -vantup | grep 5432
```

<br>

---

### No RHEL9

Como no MPSP faz-se utilização do _RedHat_, seguiu-se as intruções de instalação do [PostGreSQL](https://www.postgresql.org/download/linux/redhat/):

```shell
# Adiciona repositório
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Desabilita repo padrão
sudo dnf -qy module disable postgresql

# Instala
sudo dnf install -y postgresql16-server

# Inicia db
sudo /usr/pgsql-16/bin/postgresql-16-setup initdb
```

<br>

Os serviços para inicializar, conferir _status_ etc.

```shell
# Status
sudo systemctl status postgresql-16

# Start
sudo systemctl start postgresql-16

# Restart
sudo systemctl restart postgresql-16

# Enable
sudo systemctl enable postgresql-16
```

<br>

---

## Language: pt-BR

Antes de dar o comando para a criação do _db_, é bom conferir se o `pt_BR` está disponível. Caso não esteja, se faz necessário instalar o _locale_.

### No Ubuntu

```shell
# Confere
locale -a | grep pt_BR

# Caso negativo, instala
sudo locale-gen pt_BR.UTF-8
sudo update-locale

# Reconfigura (acho que não precisa)
# sudo dpkg-reconfigure locales
```

<br>

---

### No RHEL9

No _RHEL9_, após muito bater cabeça, encontrei como eu faço a [Instalação de suporte linguístico](https://docs.redhat.com/pt-br/documentation/red_hat_enterprise_linux/8/html/configuring_basic_system_settings/installing-language-support_working-with-langpacks).

```shell
# Avalia qual o Locale atual
localectl status

# Instala o Locale pt_BR
sudo yum install langpacks-pt_BR

# Lista Locales Disponíveis
localectl list-locales

# Define o Locale Desejado
# Nem precisa definir o idioma do sistema, basta ter presente para criar o db com o locale correto
# sudo localectl set-locale LANG=pt_BR.UTF-8
```

<br>

Após isso é necessário "restartar" o _PostgreSQL_...

<br>

---

## Extensão _pgvector_

O ANIA/Tilene depende da extensão do PostgreSQL chamada [_pgvector_](https://github.com/pgvector/pgvector). O _pgvector_ é uma extensão para o PostgreSQL que permite armazenar, indexar e consultar dados vetoriais diretamente no banco de dados.

<br>

---

### No Ubuntu

Para instalar basta seguir o que está no [README](https://github.com/pgvector/pgvector?tab=readme-ov-file#installation) do projeto.

```shell
# Instruções de instalação
cd /tmp

# No RHEL9, pode ser necessário instalar
sudo yum install git

# Clona
git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git

#
cd pgvector
make
make install # may need sudo
```

<br>

Tive alguns erros, no Ubuntu, e foi necessário também fazer o que consta em [_Missing Header_](https://github.com/pgvector/pgvector?tab=readme-ov-file#missing-header).

```shell
# Solução do fatal error: postgres.h: No such file or directory
sudo apt install postgresql-server-dev-15
```

<br>

Descobri que o _pgvector_ está em repositórios, sendo possível instalar diretamente com o [apt](https://github.com/pgvector/pgvector?tab=readme-ov-file#apt).

```shell
sudo apt install postgresql-16-pgvector
```

<br>

---

### No RHE9

Descobri que o _pgvector_ está em repositórios, sendo possível instalar diretamente com o [yum](https://github.com/pgvector/pgvector?tab=readme-ov-file#yum).

```shell
# Ajustar versão do PostGreSQL
sudo yum install pgvector_16
```

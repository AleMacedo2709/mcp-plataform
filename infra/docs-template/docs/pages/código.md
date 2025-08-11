# Código Fonte

[![Repo](https://img.shields.io/badge/GitHub-repo-blue?logo=github&logoColor=f5f5f5)](https://github.com/mpsp-br/ANIA_TCE_Core) [![Repo](https://img.shields.io/badge/Azure%20DevOps-repo-blue?logo=azuredevops&logoColor=f5f5f5)](https://dev.azure.com/mpsp/CGE/_git/ANIA_TCE_Core)

Inicialmente o código foi disponibilizado para a _Equipe de Infra_ (CTIC). Em 27.03.2025 o código foi compartilhado com _Equipe de Dados_, por meio do _repo_ [gchecon/ania_core](https://github.com/gchecon/ania_core).

<br>

!!! warning "Atenção!"

    O _repo_ [mpsp-br/ANIA_TCE_Core](https://github.com/mpsp-br/ANIA_TCE_Core) está hospedado originalmente no [GitHub](https://github.com/), visto trata-se de um _fork_ do projeto original, do TCE. O MPSP, por sua vez, usa como serviço de hospedagem de código o [Azure DevOps](https://aex.dev.azure.com/).<br><br>
    Visando institucionalizar o código na estrutura do _Azure DevOps_, foi desenvolvida uma _Git Action_ para que, a cada _push_ no _repo_ do _GitHub_, ocorre uma sincronização unidirecional para o _repo_ [CGE/ANIA_TCE_Core](https://dev.azure.com/mpsp/CGE/_git/ANIA_TCE_Core), possibilitando _deploys_. Dessa forma não se perde a vinculação ao código original (do TCE) possibilitada pelo _fork_.

!!! info "Vem somar!"

    Para entender mais por que usar o _GitHub_ e _Azure DevOps_ simultaneamente, sugiro a leitura do _post_ [Por que criar uma "organization" no GitHub não oficial?](https://github.com/orgs/mpsp-br/discussions/1). Para contribuições (_pull requests_), favor solicitar acesso ao _repo_ [mpsp-br/ANIA_TCE_Core](https://github.com/mpsp-br/ANIA_TCE_Core) à Michel Metran (SubInova) e/ou Guilherme Martelato (CTIC).

<br>

---

## IDEs sugeridas

### Para _python_

Apens a título de sugestão:

- [VsCode](https://code.visualstudio.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)

<br>

---

### Para _SQL_

#### pgAdmin [Opcional]

O [_pgAdmin_](https://www.pgadmin.org/) é uma ferramenta de administração e desenvolvimento para o _PostgreSQL_. Ele oferece uma interface gráfica intuitiva que facilita a gestão de bancos de dados, permitindo aos usuários realizar tarefas como:

- Visualização e edição de dados: Você pode adicionar, editar ou excluir registros diretamente na interface.
- Execução de consultas SQL: Permite criar, modificar e executar consultas SQL de forma eficiente.
- Gerenciamento de objetos do banco de dados: Inclui tabelas, índices, funções e muito mais.

<br>

???+ warning "Atenção"

    Não se deve instalar o [_pgAdmin_](https://www.pgadmin.org/) no _WSL_. Ele deve ser instalado diretamente no _Windows_.

<br>

---

##### Instalando no Ubuntu

Para instalar usei os comandos abaixo, também com orientação do _post_ [Install and Configure PostgreSQL and pgAdmin on Ubuntu 20.04 | 22.04](https://medium.com/yavar/install-and-configure-postgresql-and-pgadmin-on-ubuntu-20-04-22-04-52c52c249b9e).

```shell
# Atualiza pacotes
sudo apt update -y && sudo apt upgrade -y

# Adiciona Chaves
wget --quiet -O - https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg

# Adiciona Repos
echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list

# Instala
sudo apt update

# Install for both desktop and web modes:
sudo apt install pgadmin4
sudo apt uninstall pgadmin4

# Install for desktop mode only:
sudo apt install pgadmin4-desktop

# Install for web mode only:
sudo apt install pgadmin4-web
```

<br>

---

#### PSQL

PSQL é uma ferramenta de linha de comando usada para interagir com o PostgreSQL, que é um sistema de gerenciamento de banco de dados objeto-relacional de código aberto. Com o PSQL, você pode executar comandos SQL, gerenciar bancos de dados e realizar diversas operações administrativas diretamente pelo terminal.

```shell
# Viro root
sudo su

# Para entrar no usuário postgres
su - postgres

# Ou, em um comando, só...
sudo -i -u postgres

# CLI do PostGres
psql
```

<br>

Uma vez no `psql`, é possível dar os comandos.

```shell
# Lista dbs
\l

# Lista usuários
\du

# Lista tabelas
\dt
```

<br>

Por fim aplicamos o conteudo do _script_ `.sql` que usando o `psql` (há outros meios).

```shell
\connect {db_name}
\connect ania
\connect ania_logs
\connect postgres
```

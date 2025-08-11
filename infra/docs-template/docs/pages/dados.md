# Dados

## Criar <i>dbs</i>

Para criar o _db_ do Tilene com as configurações recomendadas pelo TCE basta dar o
comando abaixo. Explicação:

- `ENCODING 'UTF8'`: Define o encoding do banco de dados como UTF-8.
- `LC_COLLATE 'pt_BR.UTF-8'`: Define a ordenação de _strings_ (_collation_) para o idioma português do Brasil.
- `LC_CTYPE 'pt_BR.UTF-8'`: Define o tipo de caractere para o idioma português do Brasil.
- `TEMPLATE template0`: Garante que o banco seja criado com configurações limpas, ignorando as configurações herdadas de outros _templates_.

```sql
CREATE DATABASE tilene
WITH
    ENCODING 'UTF8'
    LC_COLLATE 'pt_BR.UTF-8'
    LC_CTYPE 'pt_BR.UTF-8'
    TEMPLATE template0;
```

<br>

Em 29.04.2025 inclui também a definição de um _db_ específico para guardar os _logs_ da aplicação.

```sql
CREATE DATABASE tilene_logs
WITH
    ENCODING 'UTF8'
    LC_COLLATE 'pt_BR.UTF-8'
    LC_CTYPE 'pt_BR.UTF-8'
    TEMPLATE template0;
```

<br>

Ainda no `psql`, é possível mudar a senha (necessário para testes). Recomenda-se evitar o uso de `@` na senha, visto que dá um _bug_ na _connection string_ devido à maneira como o TCE desenvolveu.

```sql
-- Create User
CREATE USER tilene_user;

-- Add Password (mudar a senha!)
ALTER
USER tilene_user
WITH ENCRYPTED PASSWORD 'HvS32nopNH!2zEeZ';
```

<br>

---

## Permissões

Após conectar a cada _db_, dar as devidas permissões.

```sql
-- Grant com usuário postgres
GRANT ALL PRIVILEGES ON DATABASE tilene TO tilene_user;
GRANT ALL PRIVILEGES ON DATABASE tilene_logs TO tilene_user;

GRANT USAGE ON SCHEMA public TO tilene_user;
GRANT CREATE ON SCHEMA public TO tilene_user;
GRANT ALL ON SCHEMA public TO tilene_user;

-- Grant após conectar ao db
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tilene_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tilene_user;

-- Após não entender as permissões necessárias, mandei um superuser
ALTER USER tilene_user WITH SUPERUSER;
```

<br>

---

## Estrutura dos Dados

Na pasta `./tools/data/sql/` existe o arquivo denominado `schema.sql` e `schema_logs.sql` que contém a DDL de criação do banco de dados.

No arquivo `schema.sql` existem três tabelas que devem ser criadas no _db_ `tilene`, cujo conteúdo é explicado a seguir:

1. Tabela **usuarios**: associa a identificação de usuário (chave primária) ao _e-mail_ e registra o _timestamp_ do último _login_ efetuado por este usuário.
2. Tabela **textos**: associa o usuário aos textos manipulados por ele. Os textos estão quebrados em _chunks_, com seus respectivos _embeddings_. Um mesmo usuário e texto podem ter diversas linhas nesta base de dados. O tamanho do vetor é limitado em 1536.
3. Tabela **log_uso_api**: associa o usuário e arquivo a um determinado registro de uso. Acrescenta informações como a _API_ usada (_embedding_ ou _completion_), o total de _tokens_ gerados, o nome do arquivo e a data.

<br>

No arquivo `schema_logs.sql` existe uma tabela que deve ser criada no _db_ `tilene_logs`, cujo conteúdo é explicado a seguir:

1. Tabela **logs**: armazena os logs da aplicação.

<br>

Necessário criar essas tabelas nos _dbs_ recém-instanciado.

<br>

---

### Ambiente de Desenvolvimento

Visando facilitar a criação das tabelas no _database_, está sendo usado o [Flask SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) que teve a implantação no projeto do ANIA iniciada pelo TCE. Contudo, o TCE não explorou a criação das tabelas a partir do _model_, existindo a definição das tabelas tanto no projeto do ANIA (_python_), bem como no arquivo _script.sql_.

Visando adotar um princípio similar ao "Single Source of Truth", optou-se por manter a definição das tabelas do _db_ apenas em um local. Optou-se por manter a definição no projeto, usando o [SQLALchemy](https://www.sqlalchemy.org/) e criou-se um _script python_ chamado `tools/db_create.py` para a criação do banco de dados.

???+ failure "Falha conhecida"

    O *script* não está funcionando por que estou com problemas na definição de permissões do `tilene_user`. Preciso abrir demais as permissões para que o `tilene_user` possa criar tabelas nos *dbs*.

    Para contornar, por ora, é necessário criar usando o mesmo que é indicado para o [Ambiente de Produção](#ambiente_de_producao).

<br>

É possível rodar o comando diretamente a partir da IDE, ou também pelo _shell_.

```shell
# Help
python tools/db_create.py --help

# Run
python tools/db_create.py --drop --schema db_app
python tools/db_create.py --drop --schema db_log # Não funciona
```

<br>

---

### Ambiente de Produção

Visto que no MPSP o servidor de aplicação não tem acesso aos comandos SQL do tipo _Data Definition Language_ (DML), é necessário que exista um arquivo _.sql_, contendo os comandos para a criação das tabelas, permitindo que os DBAs (_Database Administrator_) criem as tabelas "manualmente" (com auxílio do _script_).

\*[Data Definition Language]: DML é um subconjunto de comandos SQL utilizado para definir e modificar a estrutura de um banco de dados.

Dessa forma, apesar da facilidade proporcionada pelo [Flask SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/), foi necessário criar uma função que exporte as definições das tabelas, disponível no arquivo `ania/indice_ania/model.py`, para um arquivo _.sql_. Isso foi feito no módulo contido no arquivo `tools/db_export.py`.

É possível rodar o comando diretamente a partir da IDE, ou também pelo _shell_.

```shell
# Help
python tools/db_export.py --help

# Run
python tools/db_export.py --filepath './tools/data/sql/schema.sql' --schema db_app
python tools/db_export.py --filepath './tools/data/sql/schema_log.sql' --schema db_log
```

<br>

Portanto, a cada alteração do _model_ fica fácil para converter as definições do _model_ para o arquivo _.sql_.

/*---------------------------------------------------------
Script para criação dos dbs

Michel Metran
Data: 01.07.2025
Atualizado em: 04.07.2025
*/---------------------------------------------------------



/*---------------------------------------------------------
CRIA DATABASES
*/---------------------------------------------------------

-- Tudo isso fiz com o usuário postgres e db postgres...
CREATE DATABASE tilene
WITH
    ENCODING 'UTF8'
    LC_COLLATE 'pt_BR.UTF-8'
    LC_CTYPE 'pt_BR.UTF-8'
    TEMPLATE template0;


CREATE DATABASE tilene_logs
WITH
    ENCODING 'UTF8'
    LC_COLLATE 'pt_BR.UTF-8'
    LC_CTYPE 'pt_BR.UTF-8'
    TEMPLATE template0;



/*---------------------------------------------------------
CRIA USUÁRIO
*/---------------------------------------------------------

-- Create User
CREATE USER tilene_user;


-- Add Password (mudar a senha!)
ALTER
USER tilene_user
WITH ENCRYPTED PASSWORD 'HvS32nopNH!2zEeZ';



/*---------------------------------------------------------
PERMISSÕES
*/---------------------------------------------------------



REVOKE ALL ON DATABASE tilene FROM tilene_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO tilene_user;


GRANT CONNECT ON DATABASE tilene TO tilene_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO tilene_user;


-- Grant após conectar ao db tilene
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tilene_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tilene_user;

-- Dê permissão de leitura nas tabelas (opcionalmente, use SELECT, INSERT, etc.)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO tilene_user;

-- Para garantir que ele tenha acesso também a futuras tabelas:
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO tilene_user;

-- Verifique o dono do schema
SELECT schema_name, schema_owner FROM information_schema.schemata;

-- Grant com usuário postgres
GRANT ALL PRIVILEGES ON DATABASE tilene TO tilene_user;
GRANT ALL PRIVILEGES ON DATABASE tilene_logs TO tilene_user;

-- Dê acesso ao schema public
GRANT USAGE ON SCHEMA public TO tilene_user;


GRANT CREATE ON SCHEMA public TO tilene_user;
GRANT ALL ON SCHEMA public TO tilene_user;


-- Altera configurações de usuário tilene_user com usuário postgres
-- Após tentar várias permissões, sem sucesso, mandei um superuser
ALTER USER tilene_user WITH SUPERUSER;


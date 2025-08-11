/*------------------------------------------------------------
Script para criação das tabelas do ANIA
Script criado com auxílio do módulo db_export.py

Michel Metran
Data: 18.06.2025
*/------------------------------------------------------------

-- Extensão do PostgreSQL
CREATE EXTENSION IF NOT EXISTS "vector";


-- Cria tabela usuarios
CREATE TABLE IF NOT EXISTS usuarios (
	id SERIAL NOT NULL, 
	id_usuario UUID NOT NULL, 
	data_criacao TIMESTAMP WITH TIME ZONE, 
	data_ultimo_login TIMESTAMP WITH TIME ZONE, 
	CONSTRAINT pk_usuarios PRIMARY KEY (id), 
	CONSTRAINT uq_usuarios_id_usuario UNIQUE (id_usuario)
);

-- Define comentários para a usuarios
COMMENT ON TABLE usuarios IS 'Usuários que se logaram, ao menos uma vez, na aplicação';

COMMENT ON COLUMN usuarios.id IS 'Id do registro, auto incrementado';

COMMENT ON COLUMN usuarios.id_usuario IS 'Id do usuário, no formato UUID, obtido no Microsoft Entra ID';

COMMENT ON COLUMN usuarios.data_criacao IS 'Data de criação do usuário';

COMMENT ON COLUMN usuarios.data_ultimo_login IS 'Data do último login do usuário';



-- Cria tabela log_uso_api
CREATE TABLE IF NOT EXISTS log_uso_api (
	id SERIAL NOT NULL, 
	id_usuario UUID, 
	arquivo VARCHAR(300), 
	api VARCHAR(300), 
	total_tokens INTEGER, 
	data TIMESTAMP WITH TIME ZONE, 
	CONSTRAINT pk_log_uso_api PRIMARY KEY (id), 
	CONSTRAINT fk_log_uso_api_id_usuario_usuarios FOREIGN KEY(id_usuario) REFERENCES usuarios (id_usuario) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Define comentários para a log_uso_api
COMMENT ON TABLE log_uso_api IS 'Logs da utilização da API';

COMMENT ON COLUMN log_uso_api.id IS 'Id do registro, auto incrementado';

COMMENT ON COLUMN log_uso_api.id_usuario IS 'Id do usuário, no formato UUID, obtido no Microsoft Entra ID';

COMMENT ON COLUMN log_uso_api.arquivo IS 'Nome do arquivo';

COMMENT ON COLUMN log_uso_api.api IS 'API utilizada';

COMMENT ON COLUMN log_uso_api.total_tokens IS 'Total de tokens utilizados na API';

COMMENT ON COLUMN log_uso_api.data IS 'Data do log de uso da API';



-- Cria tabela textos
CREATE TABLE IF NOT EXISTS textos (
	id SERIAL NOT NULL, 
	id_usuario UUID, 
	arquivo VARCHAR(300), 
	texto TEXT, 
	num_tokens INTEGER, 
	embedding VECTOR(1536), 
	CONSTRAINT pk_textos PRIMARY KEY (id), 
	CONSTRAINT fk_textos_id_usuario_usuarios FOREIGN KEY(id_usuario) REFERENCES usuarios (id_usuario) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Define comentários para a textos
COMMENT ON TABLE textos IS 'Tabela que armazena os textos indexados no sistema';

COMMENT ON COLUMN textos.id IS 'Id do registro, auto incrementado';

COMMENT ON COLUMN textos.id_usuario IS 'Id do usuário, no formato UUID, obtido no Microsoft Entra ID';

COMMENT ON COLUMN textos.arquivo IS 'Nome do arquivo';

COMMENT ON COLUMN textos.texto IS 'Trecho do texto a ser indexado';

COMMENT ON COLUMN textos.num_tokens IS 'Número de tokens do texto';

COMMENT ON COLUMN textos.embedding IS 'Embedding do texto';




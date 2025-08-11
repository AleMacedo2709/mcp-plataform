/*------------------------------------------------------------
Script para criação da tabela de log do ANIA
Script criado com auxílio do módulo db_export.py

Michel Metran
Data: 18.06.2025
*/------------------------------------------------------------

-- Extensão do PostgreSQL
-- Por algum bug, é necessário criar a extensão "vector" mesmo que logs não utilize
CREATE EXTENSION IF NOT EXISTS "vector";


-- Cria tabela logs
CREATE TABLE IF NOT EXISTS logs (
	id SERIAL NOT NULL, 
	log_level VARCHAR(50) NOT NULL, 
	log_name VARCHAR(100) NOT NULL, 
	log_func VARCHAR(100), 
	log_message TEXT NOT NULL, 
	log_time TIMESTAMP WITH TIME ZONE NOT NULL, 
	CONSTRAINT pk_logs PRIMARY KEY (id)
);

-- Define comentários para a logs
COMMENT ON TABLE logs IS 'Tabela que armazena os logs do ANIA/Tilene';

COMMENT ON COLUMN logs.id IS 'Id do registro, auto incrementado';

COMMENT ON COLUMN logs.log_level IS 'Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)';

COMMENT ON COLUMN logs.log_name IS 'Nome do logger (ou módulo do python)';

COMMENT ON COLUMN logs.log_func IS 'Nome da função';

COMMENT ON COLUMN logs.log_message IS 'Mensagem do log';

COMMENT ON COLUMN logs.log_time IS 'Data e hora do log';




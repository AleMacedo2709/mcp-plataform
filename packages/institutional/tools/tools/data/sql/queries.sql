/*---------------------------------------------------------
Script contendo queries para analisar o db

Michel Metran
Data: 01.07.2025
Atualizado em: 04.07.2025
*/---------------------------------------------------------


/*---------------------------------------------------------
Consulta de tabela Usuarios
*/---------------------------------------------------------

SELECT
    *
FROM
    public.usuarios;


/*---------------------------------------------------------
Consulta de tabela Textos
*/---------------------------------------------------------

SELECT
    *
FROM
    public.textos;


/*---------------------------------------------------------
Consulta de tabela Log Uso API
*/---------------------------------------------------------

SELECT
    *
FROM
    public.logs
WHERE 1=1
AND log_time > '2025-06-01'
AND log_level = 'ERROR'



/*---------------------------------------------------------
Permissões
*/---------------------------------------------------------

-- For tables
SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_name = 'textos';


-- For tables
SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_name = 'logs';

-- For tables
SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_name = 'usuarios';


-- For schemas
SELECT * FROM information_schema.role_usage_grants
WHERE object_name = 'public';



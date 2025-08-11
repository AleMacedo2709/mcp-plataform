CREATE EXTENSION IF NOT EXISTS vector;


DROP TABLE IF EXISTS public.usuarios CASCADE;
CREATE TABLE IF NOT EXISTS public.usuarios
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    --email character varying(300) COLLATE pg_catalog."default" NOT NULL,
    id_usuario uuid,
    data_criacao timestamp with time zone,
    data_ultimo_login timestamp with time zone,
    CONSTRAINT user_pkey PRIMARY KEY (id),
    --CONSTRAINT unique_email UNIQUE (email)
    CONSTRAINT unique_id_usuario UNIQUE (id_usuario)
);


DROP TABLE IF EXISTS public.textos CASCADE;
CREATE TABLE IF NOT EXISTS public.textos
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    --id_usuario integer,
    id_usuario uuid,
    arquivo character varying(300) COLLATE pg_catalog."default",
    texto text COLLATE pg_catalog."default",
    num_tokens integer,
    embedding vector(1536),
    CONSTRAINT embeddings_pkey PRIMARY KEY (id),
    CONSTRAINT "fk_idUsuario" FOREIGN KEY (id_usuario)
        REFERENCES public.usuarios (id_usuario) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

DROP TABLE IF EXISTS public.log_uso_api CASCADE;
CREATE TABLE IF NOT EXISTS public.log_uso_api
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    --id_usuario integer,
    id_usuario uuid,
    arquivo character varying(300) COLLATE pg_catalog."default",
    api character varying(300) COLLATE pg_catalog."default",
    total_tokens integer,
    data timestamp with time zone,
    CONSTRAINT log_pkey PRIMARY KEY (id),
    CONSTRAINT fk_id_usuario FOREIGN KEY (id_usuario)
        REFERENCES public.usuarios (id_usuario) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

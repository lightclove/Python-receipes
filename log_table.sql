-- Database: postgres
-- DROP DATABASE postgres;
CREATE DATABASE postgres
WITH OWNER = postgres
ENCODING = 'UTF8'
TABLESPACE = pg_default
LC_COLLATE = 'Russian_Russia.1251'
LC_CTYPE = 'Russian_Russia.1251'
CONNECTION LIMIT = -1;
COMMENT ON DATABASE postgres
IS 'default administrative connection database';
---------------------------------------------------------------------------------------------------
-- Table: public.log
-- DROP TABLE public.log;
CREATE TABLE public.log
(
    id bigint NOT NULL DEFAULT nextval('log_id_seq'::regclass),
    log_level integer NOT NULL,
    log_levelname character(32),
    log_ character(2048) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by character(32) NOT NULL,
    CONSTRAINT log_pk PRIMARY KEY (id)
)
    WITH (
    OIDS=FALSE
         );
ALTER TABLE public.log
    OWNER TO postgres;
COMMENT ON TABLE public.log
IS 'For the storing logs of the Ripex_Interaction';
---------------------------------------------------------------------------------------------------
--INSERT EXAMPLE--
INSERT INTO "public"."log" ("id", "log_level", "log_levelname", "log_", "created_at", "created_by") VALUES (1, null, 'test_string', 'test_string', null, 'test_string')
--
-- PostgreSQL database dump
--

-- Dumped from database version 10.11 (Ubuntu 10.11-1.pgdg16.04+1)
-- Dumped by pg_dump version 10.11 (Ubuntu 10.11-1.pgdg16.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: gender; Type: TYPE; Schema: public; Owner: pl704206
--

CREATE TYPE public.gender AS ENUM (
    'male',
    'female'
);


ALTER TYPE public.gender OWNER TO pl704206;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: actor; Type: TABLE; Schema: public; Owner: pl704206
--

CREATE TABLE public.actor (
    id integer NOT NULL,
    name character varying(255),
    age integer,
    gender public.gender
);


ALTER TABLE public.actor OWNER TO pl704206;

--
-- Name: actor_id_seq; Type: SEQUENCE; Schema: public; Owner: pl704206
--

CREATE SEQUENCE public.actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actor_id_seq OWNER TO pl704206;

--
-- Name: actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pl704206
--

ALTER SEQUENCE public.actor_id_seq OWNED BY public.actor.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: pl704206
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO pl704206;

--
-- Name: association; Type: TABLE; Schema: public; Owner: pl704206
--

CREATE TABLE public.association (
    movie_id integer,
    actor_id integer
);


ALTER TABLE public.association OWNER TO pl704206;

--
-- Name: movie; Type: TABLE; Schema: public; Owner: pl704206
--

CREATE TABLE public.movie (
    id integer NOT NULL,
    title character varying(255),
    date_release date
);


ALTER TABLE public.movie OWNER TO pl704206;

--
-- Name: movie_id_seq; Type: SEQUENCE; Schema: public; Owner: pl704206
--

CREATE SEQUENCE public.movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movie_id_seq OWNER TO pl704206;

--
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pl704206
--

ALTER SEQUENCE public.movie_id_seq OWNED BY public.movie.id;


--
-- Name: actor id; Type: DEFAULT; Schema: public; Owner: pl704206
--

ALTER TABLE ONLY public.actor ALTER COLUMN id SET DEFAULT nextval('public.actor_id_seq'::regclass);


--
-- Name: movie id; Type: DEFAULT; Schema: public; Owner: pl704206
--

ALTER TABLE ONLY public.movie ALTER COLUMN id SET DEFAULT nextval('public.movie_id_seq'::regclass);


--
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: pl704206
--

COPY public.actor (id, name, age, gender) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: pl704206
--

COPY public.alembic_version (version_num) FROM stdin;
e6b70ef50c6b
\.


--
-- Data for Name: association; Type: TABLE DATA; Schema: public; Owner: pl704206
--

COPY public.association (movie_id, actor_id) FROM stdin;
\.


--
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: pl704206
--

COPY public.movie (id, title, date_release) FROM stdin;
\.


--
-- Name: actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pl704206
--

SELECT pg_catalog.setval('public.actor_id_seq', 26, true);


--
-- Name: movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pl704206
--

SELECT pg_catalog.setval('public.movie_id_seq', 9, true);


--
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: pl704206
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: pl704206
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: pl704206
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);


--
-- Name: association association_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pl704206
--

ALTER TABLE ONLY public.association
    ADD CONSTRAINT association_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actor(id);


--
-- Name: association association_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pl704206
--

ALTER TABLE ONLY public.association
    ADD CONSTRAINT association_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movie(id);


--
-- PostgreSQL database dump complete
--


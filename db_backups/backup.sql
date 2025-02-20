--
-- PostgreSQL database dump
--

-- Dumped from database version 14.16 (Homebrew)
-- Dumped by pg_dump version 14.16 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: consultant_roles; Type: TABLE; Schema: public; Owner: openpsa_user
--

CREATE TABLE public.consultant_roles (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.consultant_roles OWNER TO openpsa_user;

--
-- Name: consultant_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: openpsa_user
--

CREATE SEQUENCE public.consultant_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.consultant_roles_id_seq OWNER TO openpsa_user;

--
-- Name: consultant_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openpsa_user
--

ALTER SEQUENCE public.consultant_roles_id_seq OWNED BY public.consultant_roles.id;


--
-- Name: resource_allocations; Type: TABLE; Schema: public; Owner: openpsa_user
--

CREATE TABLE public.resource_allocations (
    id integer NOT NULL,
    user_id integer NOT NULL,
    project_id integer NOT NULL,
    status public.resourceallocationstatus NOT NULL,
    created_at timestamp without time zone,
    role_id integer
);


ALTER TABLE public.resource_allocations OWNER TO openpsa_user;

--
-- Name: resource_allocations_id_seq; Type: SEQUENCE; Schema: public; Owner: openpsa_user
--

CREATE SEQUENCE public.resource_allocations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.resource_allocations_id_seq OWNER TO openpsa_user;

--
-- Name: resource_allocations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openpsa_user
--

ALTER SEQUENCE public.resource_allocations_id_seq OWNED BY public.resource_allocations.id;


--
-- Name: consultant_roles id; Type: DEFAULT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.consultant_roles ALTER COLUMN id SET DEFAULT nextval('public.consultant_roles_id_seq'::regclass);


--
-- Name: resource_allocations id; Type: DEFAULT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.resource_allocations ALTER COLUMN id SET DEFAULT nextval('public.resource_allocations_id_seq'::regclass);


--
-- Data for Name: consultant_roles; Type: TABLE DATA; Schema: public; Owner: openpsa_user
--

COPY public.consultant_roles (id, name, description, created_at) FROM stdin;
1	JUNIOR	Junior Consultant	\N
2	MID	Mid Level Consultant	\N
3	SENIOR	Senior Consultant	\N
4	MASTER	Master Consultant	\N
5	PRINCIPAL	Principal Consultant	\N
\.


--
-- Data for Name: resource_allocations; Type: TABLE DATA; Schema: public; Owner: openpsa_user
--

COPY public.resource_allocations (id, user_id, project_id, status, created_at, role_id) FROM stdin;
1	2	1	PLANNED	\N	\N
2	2	1	PLANNED	\N	\N
\.


--
-- Name: consultant_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: openpsa_user
--

SELECT pg_catalog.setval('public.consultant_roles_id_seq', 1, false);


--
-- Name: resource_allocations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: openpsa_user
--

SELECT pg_catalog.setval('public.resource_allocations_id_seq', 2, true);


--
-- Name: consultant_roles consultant_roles_name_key; Type: CONSTRAINT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.consultant_roles
    ADD CONSTRAINT consultant_roles_name_key UNIQUE (name);


--
-- Name: consultant_roles consultant_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.consultant_roles
    ADD CONSTRAINT consultant_roles_pkey PRIMARY KEY (id);


--
-- Name: resource_allocations resource_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.resource_allocations
    ADD CONSTRAINT resource_allocations_pkey PRIMARY KEY (id);


--
-- Name: resource_allocations resource_allocations_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.resource_allocations
    ADD CONSTRAINT resource_allocations_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: resource_allocations resource_allocations_project_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.resource_allocations
    ADD CONSTRAINT resource_allocations_project_id_fkey1 FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: resource_allocations resource_allocations_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.resource_allocations
    ADD CONSTRAINT resource_allocations_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.consultant_roles(id);


--
-- Name: resource_allocations resource_allocations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openpsa_user
--

ALTER TABLE ONLY public.resource_allocations
    ADD CONSTRAINT resource_allocations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--


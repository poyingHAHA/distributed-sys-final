--
-- PostgreSQL database dump
--

-- Dumped from database version 13.18 (Debian 13.18-1.pgdg120+1)
-- Dumped by pg_dump version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO "user";

--
-- Name: checkins; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.checkins (
    checkin_id integer NOT NULL,
    team_id integer,
    user_id integer,
    post_url character varying(255) NOT NULL,
    checkin_time timestamp without time zone,
    round_id integer NOT NULL
);


ALTER TABLE public.checkins OWNER TO "user";

--
-- Name: checkins_checkin_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.checkins_checkin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.checkins_checkin_id_seq OWNER TO "user";

--
-- Name: checkins_checkin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.checkins_checkin_id_seq OWNED BY public.checkins.checkin_id;


--
-- Name: team_checkin_history; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.team_checkin_history (
    id integer NOT NULL,
    team_id integer NOT NULL,
    completed_at timestamp without time zone,
    member_count integer NOT NULL,
    round_id integer NOT NULL
);


ALTER TABLE public.team_checkin_history OWNER TO "user";

--
-- Name: team_checkin_history_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.team_checkin_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.team_checkin_history_id_seq OWNER TO "user";

--
-- Name: team_checkin_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.team_checkin_history_id_seq OWNED BY public.team_checkin_history.id;


--
-- Name: team_members; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.team_members (
    team_id integer NOT NULL,
    user_id integer NOT NULL,
    joined_at timestamp without time zone
);


ALTER TABLE public.team_members OWNER TO "user";

--
-- Name: teams; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.teams (
    team_id integer NOT NULL,
    team_name character varying(100) NOT NULL,
    creator_id integer,
    created_at timestamp without time zone,
    is_active boolean,
    current_score double precision,
    current_round_id integer
);


ALTER TABLE public.teams OWNER TO "user";

--
-- Name: teams_team_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.teams_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teams_team_id_seq OWNER TO "user";

--
-- Name: teams_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.teams_team_id_seq OWNED BY public.teams.team_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp without time zone,
    last_checkin_time timestamp without time zone
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: checkins checkin_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.checkins ALTER COLUMN checkin_id SET DEFAULT nextval('public.checkins_checkin_id_seq'::regclass);


--
-- Name: team_checkin_history id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.team_checkin_history ALTER COLUMN id SET DEFAULT nextval('public.team_checkin_history_id_seq'::regclass);


--
-- Name: teams team_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.teams ALTER COLUMN team_id SET DEFAULT nextval('public.teams_team_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: checkins checkins_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.checkins
    ADD CONSTRAINT checkins_pkey PRIMARY KEY (checkin_id);


--
-- Name: team_checkin_history team_checkin_history_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.team_checkin_history
    ADD CONSTRAINT team_checkin_history_pkey PRIMARY KEY (id);


--
-- Name: team_members team_members_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_pkey PRIMARY KEY (team_id, user_id);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: checkins checkins_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.checkins
    ADD CONSTRAINT checkins_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: checkins checkins_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.checkins
    ADD CONSTRAINT checkins_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: team_checkin_history team_checkin_history_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.team_checkin_history
    ADD CONSTRAINT team_checkin_history_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: team_members team_members_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(team_id);


--
-- Name: team_members team_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: teams teams_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--


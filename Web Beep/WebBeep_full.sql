--
-- PostgreSQL database dump
--

\restrict GXTu2qU0x3HFZ17dPzsFrJHYgXB7jIETQsuxWwKljvWkXNDFGi53rLFKX9XTrsD

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: WebBeep; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "WebBeep" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';


ALTER DATABASE "WebBeep" OWNER TO postgres;

\unrestrict GXTu2qU0x3HFZ17dPzsFrJHYgXB7jIETQsuxWwKljvWkXNDFGi53rLFKX9XTrsD
\connect "WebBeep"
\restrict GXTu2qU0x3HFZ17dPzsFrJHYgXB7jIETQsuxWwKljvWkXNDFGi53rLFKX9XTrsD

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: Event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Event" (
    eventid integer NOT NULL,
    eventname character varying(255),
    category character varying(255),
    status character varying(255),
    eventtime time without time zone,
    creatorid integer NOT NULL,
    locationid integer NOT NULL
);


ALTER TABLE public."Event" OWNER TO postgres;

--
-- Name: Event_creatorid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Event_creatorid_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Event_creatorid_seq" OWNER TO postgres;

--
-- Name: Event_creatorid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Event_creatorid_seq" OWNED BY public."Event".creatorid;


--
-- Name: Event_eventid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Event_eventid_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Event_eventid_seq" OWNER TO postgres;

--
-- Name: Event_eventid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Event_eventid_seq" OWNED BY public."Event".eventid;


--
-- Name: Event_locationid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Event_locationid_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Event_locationid_seq" OWNER TO postgres;

--
-- Name: Event_locationid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Event_locationid_seq" OWNED BY public."Event".locationid;


--
-- Name: Location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Location" (
    locationid integer NOT NULL,
    locationname character varying(255),
    locationaddress character varying(255)
);


ALTER TABLE public."Location" OWNER TO postgres;

--
-- Name: Location_locationid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Location_locationid_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Location_locationid_seq" OWNER TO postgres;

--
-- Name: Location_locationid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Location_locationid_seq" OWNED BY public."Location".locationid;


--
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    user_id integer NOT NULL,
    firstname character varying(255),
    lastname character varying(255),
    username character varying(255),
    password character varying(255),
    creatorid integer NOT NULL
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- Name: User_creatorid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_creatorid_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."User_creatorid_seq" OWNER TO postgres;

--
-- Name: User_creatorid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_creatorid_seq" OWNED BY public."User".creatorid;


--
-- Name: User_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."User_user_id_seq" OWNER TO postgres;

--
-- Name: User_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_user_id_seq" OWNED BY public."User".user_id;


--
-- Name: Event eventid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event" ALTER COLUMN eventid SET DEFAULT nextval('public."Event_eventid_seq"'::regclass);


--
-- Name: Event creatorid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event" ALTER COLUMN creatorid SET DEFAULT nextval('public."Event_creatorid_seq"'::regclass);


--
-- Name: Event locationid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event" ALTER COLUMN locationid SET DEFAULT nextval('public."Event_locationid_seq"'::regclass);


--
-- Name: Location locationid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Location" ALTER COLUMN locationid SET DEFAULT nextval('public."Location_locationid_seq"'::regclass);


--
-- Name: User user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN user_id SET DEFAULT nextval('public."User_user_id_seq"'::regclass);


--
-- Name: User creatorid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN creatorid SET DEFAULT nextval('public."User_creatorid_seq"'::regclass);


--
-- Data for Name: Event; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."Event" VALUES (1, 'Quarterly Meeting', 'Work', 'Uncomplete', '10:30:00', 1, 1);
INSERT INTO public."Event" VALUES (2, 'Lunch Meeting', 'Work', 'Complete', '10:30:00', 1, 2);
INSERT INTO public."Event" VALUES (3, 'Doctor Appointment', 'Personal', 'Uncomplete', '10:30:00', 6, 3);
INSERT INTO public."Event" VALUES (4, 'Zoom Meeting', 'Work', 'Complete', '10:30:00', 8, 4);
INSERT INTO public."Event" VALUES (5, 'Algorithms Class', 'School', 'Complete', '10:30:00', 2, 5);
INSERT INTO public."Event" VALUES (6, 'Meeting with CEO', 'Work', 'Complete', '10:30:00', 3, 6);
INSERT INTO public."Event" VALUES (7, 'Study Session', 'School', 'Uncomplete', '10:30:00', 5, 7);


--
-- Data for Name: Location; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."Location" VALUES (1, 'Oakland University', '201 Meadow Brook Rd, Rochester, MI 48309');
INSERT INTO public."Location" VALUES (2, 'Zoom', 'https://zoom.us');
INSERT INTO public."Location" VALUES (3, 'Work Office', '49675 Van Dyke Ave, Shelby Township, MI 48317');
INSERT INTO public."Location" VALUES (4, 'Da Francescas', ' 49521 Van Dyke Ave, Shelby Township, MI 48317');
INSERT INTO public."Location" VALUES (5, 'Henry Ford Hospital', '2799 W Grand Blvd, Detroit, MI 48202');
INSERT INTO public."Location" VALUES (6, 'CEO Office', 'One Apple Park Way, Cupertino, CA 95014');
INSERT INTO public."Location" VALUES (7, 'Auburn Hills Library', '3400 E Seyburn Dr, Auburn Hills, MI 48326');


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."User" VALUES (1, 'John', 'Doe', 'Username1', 'Password1', 1);
INSERT INTO public."User" VALUES (2, 'Sarah', 'Robinson', 'Username2', 'Password2', 2);
INSERT INTO public."User" VALUES (3, 'Jane', 'Wilson', 'JWilson', 'P@ssword', 3);
INSERT INTO public."User" VALUES (4, 'Taylor', 'Swift', 'TaySwift', 'Kelce<3Taylor', 4);
INSERT INTO public."User" VALUES (5, 'Brandon', 'Mercado Franco', 'bmercadofranco', 'Password3', 5);
INSERT INTO public."User" VALUES (6, 'Owen', 'Klochack', 'OKlochack', 'Password4', 6);
INSERT INTO public."User" VALUES (7, 'Madison', 'Latimer', 'MLatimer', 'Password5', 7);
INSERT INTO public."User" VALUES (8, 'Zachary', 'Wood', 'ZWood', 'Password6', 8);
INSERT INTO public."User" VALUES (9, 'Firma', 'Strumban', 'FStrumban', 'Password7', 9);


--
-- Name: Event_creatorid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Event_creatorid_seq"', 1, false);


--
-- Name: Event_eventid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Event_eventid_seq"', 7, true);


--
-- Name: Event_locationid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Event_locationid_seq"', 7, true);


--
-- Name: Location_locationid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Location_locationid_seq"', 7, true);


--
-- Name: User_creatorid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."User_creatorid_seq"', 9, true);


--
-- Name: User_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."User_user_id_seq"', 9, true);


--
-- Name: Event Event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (eventid);


--
-- Name: Location Location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Location"
    ADD CONSTRAINT "Location_pkey" PRIMARY KEY (locationid);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_id);


--
-- Name: User creatorid_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT creatorid_unique UNIQUE (creatorid);


--
-- Name: Location locationid_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Location"
    ADD CONSTRAINT locationid_unique UNIQUE (locationid);


--
-- Name: Event fk_creatorid; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT fk_creatorid FOREIGN KEY (creatorid) REFERENCES public."User"(creatorid);


--
-- Name: Event fk_locationid; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT fk_locationid FOREIGN KEY (locationid) REFERENCES public."Location"(locationid);


--
-- PostgreSQL database dump complete
--

\unrestrict GXTu2qU0x3HFZ17dPzsFrJHYgXB7jIETQsuxWwKljvWkXNDFGi53rLFKX9XTrsD


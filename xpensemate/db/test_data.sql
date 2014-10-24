--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2014-10-23 17:29:52 PDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET session_replication_role = replica;

SET search_path = public, pg_catalog;

--
-- TOC entry 1979 (class 0 OID 17086)
-- Dependencies: 173
-- Data for Name: table_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_group (id, name) FROM stdin;
1	Cosa nostra
\.


--
-- TOC entry 1982 (class 0 OID 17109)
-- Dependencies: 176
-- Data for Name: table_expense; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_expense (id, date, description, amount, group_id) FROM stdin;
1	2014-10-21	First expense	10.00	1
2	2014-10-21	Second expense	15.00	1
\.


--
-- TOC entry 1988 (class 0 OID 0)
-- Dependencies: 175
-- Name: table_expense_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_expense_id_seq', 2, true);


--
-- TOC entry 1977 (class 0 OID 17072)
-- Dependencies: 171
-- Data for Name: table_member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_member (id, name, password_hash, password_salt, active) FROM stdin;
1	Dana	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	t
2	Andy	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	t
3	Victoria	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	t
4	Jack	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	\\x09fb9ff32c5aa81bf3cd060e82f8bdfe6fa40b933c00a3b83094a4a6a9c1db24	t
\.


--
-- TOC entry 1983 (class 0 OID 17123)
-- Dependencies: 177
-- Data for Name: table_expense_member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_expense_member (expense_id, member_id, made_expense) FROM stdin;
1	1	t
1	2	f
1	3	f
2	2	t
2	1	f
\.


--
-- TOC entry 1989 (class 0 OID 0)
-- Dependencies: 172
-- Name: table_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_group_id_seq', 1, true);


--
-- TOC entry 1980 (class 0 OID 17092)
-- Dependencies: 174
-- Data for Name: table_member_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_member_group (member_id, group_id) FROM stdin;
1	1
2	1
3	1
\.


--
-- TOC entry 1990 (class 0 OID 0)
-- Dependencies: 170
-- Name: table_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_member_id_seq', 4, true);


-- Completed on 2014-10-23 17:29:52 PDT

--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2014-10-24 15:30:41 PDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET session_replication_role = replica;

SET search_path = public, pg_catalog;

--
-- TOC entry 2029 (class 0 OID 17269)
-- Dependencies: 173
-- Data for Name: table_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_group (id, name) FROM stdin;
1	Cosa nostra
\.


--
-- TOC entry 2032 (class 0 OID 17292)
-- Dependencies: 176
-- Data for Name: table_expense; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_expense (id, date_info, description, amount, group_id) FROM stdin;
1	2014-10-21	First expense	10.00	1
2	2014-10-21	Second expense	15.00	1
3	2014-10-21	Third expense	15.00	1
\.


--
-- TOC entry 2038 (class 0 OID 0)
-- Dependencies: 175
-- Name: table_expense_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_expense_id_seq', 3, true);


--
-- TOC entry 2027 (class 0 OID 17255)
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
-- TOC entry 2033 (class 0 OID 17306)
-- Dependencies: 177
-- Data for Name: table_expense_member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_expense_member (expense_id, member_id, made_expense) FROM stdin;
1	1	t
1	2	f
1	3	f
2	2	t
2	1	f
3	2	f
3	1	t
\.


--
-- TOC entry 2039 (class 0 OID 0)
-- Dependencies: 172
-- Name: table_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_group_id_seq', 1, true);


--
-- TOC entry 2030 (class 0 OID 17275)
-- Dependencies: 174
-- Data for Name: table_member_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_member_group (member_id, group_id, is_owner) FROM stdin;
2	1	f
3	1	f
1	1	t
\.


--
-- TOC entry 2040 (class 0 OID 0)
-- Dependencies: 170
-- Name: table_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_member_id_seq', 4, true);


-- Completed on 2014-10-24 15:30:41 PDT

--
-- PostgreSQL database dump complete
--


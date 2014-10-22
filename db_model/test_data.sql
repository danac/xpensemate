--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;
SET session_replication_role = replica;
--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "table_group" (id, name) FROM stdin;
1	Cosa nostra
\.


--
-- Data for Name: expense; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_expense (id, date, description, amount, group_id) FROM stdin;
1	2014-10-21	First expense	10.00	1
2	2014-10-21	Second expense	15.00	1
\.


--
-- Name: expense_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_expense_id_seq', 2, true);


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_member (id, name) FROM stdin;
1	Dana
2	Andy
3	Victoria
4	Jack
\.


--
-- Data for Name: expense_member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_expense_member (expense_id, member_id, made_expense) FROM stdin;
1	1	t
1	2	f
1	3	f
2	2	t
2	1	f
\.


--
-- Name: group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_group_id_seq', 1, true);


--
-- Data for Name: member_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY table_member_group (member_id, group_id) FROM stdin;
1	1
2	1
3	1
\.


--
-- Name: member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('table_member_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--


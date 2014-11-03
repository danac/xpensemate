-- Copyright 2014 Dana Christen
--
-- This file is part of XpenseMate, a tool for managing shared expenses and
-- hosted at https://github.com/danac/xpensemate.
--
-- XpenseMate is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as
-- published by the Free Software Foundation, either version 3 of the
-- License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program. If not, see <http://www.gnu.org/licenses/>.
--


-- REVOKE ALL PRIVILEGES ON DATABASE xpensemate FROM PUBLIC;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;

GRANT EXECUTE ON FUNCTION get_user(VARCHAR) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION get_groups(INTEGER) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION get_group_members(INTEGER) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION get_group_expenses(INTEGER) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION get_group_transfers(INTEGER) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION get_member_balance(INTEGER, INTEGER) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION get_group_balances(INTEGER) TO xpensemate_function_invoker;

GRANT EXECUTE ON FUNCTION insert_member(VARCHAR, VARCHAR, VARCHAR) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION insert_group(VARCHAR, INTEGER, VARIADIC INTEGER[]) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION insert_group_member(INTEGER, INTEGER) TO xpensemate_function_invoker;
GRANT EXECUTE ON FUNCTION delete_expense(INTEGER) TO xpensemate_function_invoker;

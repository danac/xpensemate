
--
-- GETTER FUNCTIONS
--

--- List the members of a group with their overall balance in the group
DROP TYPE IF EXISTS member_credential_t CASCADE;
CREATE TYPE member_credential_t AS (id INTEGER, name VARCHAR, password_hash VARCHAR, password_salt VARCHAR);
CREATE OR REPLACE FUNCTION get_user(name VARCHAR)
    RETURNS SETOF member_credential_t AS
    $BODY$
        SELECT id, name, ENCODE(password_hash, 'base64'), ENCODE(password_salt, 'base64')
        FROM table_member
        WHERE name = $1 AND active IS TRUE
    $BODY$
    LANGUAGE 'sql';


--- List the groups of a given member, based on a member id
CREATE OR REPLACE FUNCTION get_groups(member_id INTEGER)
    RETURNS SETOF table_group AS
    $BODY$
        SELECT table_group.id, table_group.name
        FROM table_member_group
        INNER JOIN table_group ON table_group.id = table_member_group.group_id
        WHERE table_member_group.member_id = $1
    $BODY$
    LANGUAGE 'sql';


--- List the groups of a given member, based on a member name
--CREATE OR REPLACE FUNCTION get_groups(member_name VARCHAR)
    --RETURNS SETOF table_group AS
    --$BODY$
        --DECLARE
            --member_id INTEGER;
        --BEGIN
            --member_id = (SELECT id FROM table_member WHERE name = $1);
            --RETURN QUERY SELECT * FROM get_groups(member_id);
        --END
    --$BODY$
    --LANGUAGE 'plpgsql'

--- List the members of a group, based on a group id
DROP TYPE IF EXISTS member_t CASCADE;
CREATE TYPE member_t AS (id INTEGER, name VARCHAR);
CREATE OR REPLACE FUNCTION get_group_members(group_id INTEGER)
    RETURNS SETOF member_t AS
    $BODY$
        SELECT table_member.id, table_member.name
        FROM table_member_group
        INNER JOIN table_member ON table_member_group.member_id = table_member.id
        WHERE table_member_group.group_id = $1
    $BODY$
    LANGUAGE 'sql';


--- List the expenses of a group
DROP TYPE IF EXISTS expense_t CASCADE;
CREATE TYPE expense_t AS (id INTEGER, date_info DATE, description VARCHAR, amount NUMERIC, member_names VARCHAR);
CREATE OR REPLACE FUNCTION get_group_expenses(group_id INTEGER)
    RETURNS SETOF expense_t AS
    $BODY$
        SELECT table_expense.id, table_expense.date_info, table_expense.description, table_expense.amount, string_agg(table_member.name, '|') AS expense_members
        FROM table_expense_member
        INNER JOIN table_member ON table_member.id = table_expense_member.member_id
        INNER JOIN table_expense on table_expense.id = table_expense_member.expense_id
        WHERE table_expense.group_id=$1
        GROUP BY table_expense.id
    $BODY$
    LANGUAGE 'sql';

--- Get the balance of a given member in a given group
CREATE OR REPLACE FUNCTION get_member_balance(member_id INTEGER, group_id INTEGER)
    RETURNS NUMERIC AS
    $BODY$
        --- Difference of the amounts to pay and already paid
        SELECT amount_to_pay_agg.amount_to_pay - COALESCE(paid_amount_agg.paid_amount, 0.0) AS balance
        FROM (
            --- Aggregation of the total amount of the selected expenses
            --- weighted by the number of members involved in each expense
            SELECT SUM(table_expense.amount / num_members_agg.num_members) AS amount_to_pay
            FROM (
                --- Count of the number of members in the expenses
                SELECT table_expense_member.expense_id, COUNT(table_expense_member.member_id) AS num_members
                FROM table_expense_member
                WHERE table_expense_member.expense_id IN (
                    --- Expense IDs matching the member and the group
                    SELECT table_expense.id AS expense_id
                    FROM table_expense
                    INNER JOIN table_expense_member ON table_expense_member.expense_id = table_expense.id
                    WHERE table_expense.group_id = $2 AND table_expense_member.member_id = $1
                )
                GROUP BY table_expense_member.expense_id
            ) AS num_members_agg
            --- Link to the expense table based on the expenses for which the number of members was aggregated
            INNER JOIN table_expense ON num_members_agg.expense_id = table_expense.id
        ) AS amount_to_pay_agg,
        (
            --- Expense IDs matching the member and the group, for which the member actually made the expense,
            --- and aggregation of the total amount
            SELECT SUM(table_expense.amount) AS paid_amount
            FROM table_expense
            INNER JOIN table_expense_member ON table_expense_member.expense_id = table_expense.id
            WHERE table_expense.group_id = $2 AND table_expense_member.member_id = $1 AND table_expense_member.made_expense IS TRUE
        ) AS paid_amount_agg
    $BODY$
    LANGUAGE 'sql';
    

--- List the balances of all members of a group
DROP TYPE IF EXISTS member_balance_t CASCADE;
CREATE TYPE member_balance_t AS (member_id INTEGER, balance numeric);
CREATE OR REPLACE FUNCTION get_group_balances(group_id INTEGER)
    RETURNS SETOF member_balance_t AS
    $BODY$
        DECLARE
            member_id INTEGER;
            result_row member_balance_t;
        BEGIN
            FOR member_id IN (
                SELECT table_member_group.member_id
                FROM table_member_group
                WHERE table_member_group.group_id = $1
            )
            LOOP
                result_row.member_id = member_id;
                result_row.balance = get_member_balance(member_id, $1);
                RETURN NEXT result_row;
            END LOOP;
            RETURN;
        END
    $BODY$
    LANGUAGE 'plpgsql';


--
-- SETTER FUNCTIONS
--


--- Create a new group
CREATE OR REPLACE FUNCTION insert_member(member_name VARCHAR, member_password_hash VARCHAR, member_password_salt VARCHAR)
    RETURNS INTEGER AS
    $BODY$
        DECLARE
            member_id INTEGER;
        BEGIN
            INSERT INTO table_member (name, password_hash, password_salt) VALUES (QUOTE_LITERAL($1), DECODE($2, 'base64'), DECODE($3, 'base64'));
            member_id := (SELECT currval(pg_get_serial_sequence('table_member', 'id')));
            RETURN member_id;
        END
    $BODY$
    LANGUAGE 'plpgsql';
    
    
--- Create a new group
CREATE OR REPLACE FUNCTION insert_group(name VARCHAR, owner_id INTEGER, other_members VARIADIC INTEGER[])
    RETURNS INTEGER AS
    $BODY$
        DECLARE
            group_id INTEGER;
            other_member_id INTEGER;
        BEGIN
            INSERT INTO table_group (name) VALUES (QUOTE_LITERAL($1));
            group_id := (SELECT currval(pg_get_serial_sequence('table_group', 'id')));
            INSERT INTO table_member_group (member_id, group_id, is_owner) VALUES ($2, group_id, TRUE);
            FOR other_member_id IN (SELECT i FROM UNNEST($3) AS i )
            LOOP
                INSERT INTO table_member_group (member_id, group_id, is_owner) VALUES (other_member_id, group_id, FALSE);
            END LOOP;
            RETURN group_id;
        END
    $BODY$
    LANGUAGE 'plpgsql';
    
    
--- Create a new group member
CREATE OR REPLACE FUNCTION insert_group_member(new_member_id INTEGER, target_group_id INTEGER)
    RETURNS VOID AS
    $BODY$
        INSERT INTO table_member_group (member_id, group_id, is_owner) VALUES ($1, $2, FALSE);
    $BODY$
    LANGUAGE 'sql';

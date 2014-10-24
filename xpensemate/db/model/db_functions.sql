
--
-- FUNCTIONS
--

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
    

--- List the members of a group with their overall balance in the group
DROP TYPE IF EXISTS member_balance CASCADE;
CREATE TYPE member_balance AS (member_id INTEGER, balance numeric);
CREATE OR REPLACE FUNCTION get_group_balances(group_id INTEGER)
    RETURNS SETOF member_balance AS
    $BODY$
        DECLARE
            member_id INTEGER;
            result_row member_balance;
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


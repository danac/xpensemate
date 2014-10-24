--
-- VIEWS
--

--- List all expenses with human-readable member names
CREATE OR REPLACE VIEW view_expense_with_member_names AS
    SELECT table_expense.*, expense_member_agg.expense_members
    FROM (
        SELECT table_expense_member.expense_id, string_agg(table_member.name, '|') AS expense_members
        FROM table_expense_member
        INNER JOIN table_member ON table_member.id = table_expense_member.member_id
        GROUP BY table_expense_member.expense_id)
    AS expense_member_agg
    INNER JOIN table_expense ON expense_member_agg.expense_id = table_expense.id;

--- List all expenses with the number of members concerned by each of them
CREATE OR REPLACE VIEW view_expense_num_members AS
    SELECT table_expense_member.expense_id, COUNT(table_expense_member.member_id) AS num_members
    FROM table_expense_member
    GROUP BY table_expense_member.expense_id;

--- List all expenses with the amount to be paid by each of the members of the expenses
CREATE OR REPLACE VIEW view_expense_shared_amount AS
    SELECT table_expense.id AS expense_id,
           table_expense.group_id,
           members_agg.num_members,
           table_expense.amount,
           table_expense.amount / members_agg.num_members AS shared_amount
    FROM (
        SELECT table_expense_member.expense_id, COUNT(table_expense_member.member_id) AS num_members
        FROM table_expense_member
        --- Un-comment to filter the expenses listed based on a group ID
        ---WHERE table_expense_member.expense_id IN (SELECT table_expense.id FROM table_expense WHERE table_expense.group_id = 1)
        GROUP BY table_expense_member.expense_id
    ) AS members_agg
    INNER JOIN table_expense ON members_agg.expense_id = table_expense.id;

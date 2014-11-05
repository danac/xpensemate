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


--
-- GETTER FUNCTIONS
--


-- List the details of a member
DROP TYPE IF EXISTS member_credential_t CASCADE;
CREATE TYPE member_credential_t AS (
    name VARCHAR,
    password_hash VARCHAR,
    password_salt VARCHAR,
    active BOOLEAN);
CREATE OR REPLACE FUNCTION get_member(name VARCHAR)
    RETURNS SETOF member_credential_t AS
    $BODY$
        SELECT
            name,
            ENCODE(password_hash, 'base64'),
            ENCODE(password_salt, 'base64'),
            active
        FROM table_member
        WHERE name = $1
            AND active IS TRUE
    $BODY$
    LANGUAGE 'sql'
    SECURITY DEFINER;


-- List the groups of a given member, based on a member name
CREATE OR REPLACE FUNCTION get_groups(member_name VARCHAR)
    RETURNS SETOF table_group AS
    $BODY$
        SELECT
            table_group.id AS group_id,
            table_group.name AS group_name
        FROM table_member_group
        INNER JOIN table_group
            ON table_group.id = table_member_group.group_id
        INNER JOIN table_member
            ON table_member_group.member_id = table_member.id
        WHERE table_member.name = $1
    $BODY$
    LANGUAGE 'sql'
    SECURITY DEFINER;


-- List the members of a group, based on a group name
--DROP TYPE IF EXISTS group_member_t CASCADE;
--CREATE TYPE group_member_t AS (
    --name VARCHAR,
    --is_owner BOOLEAN);
--CREATE OR REPLACE FUNCTION get_group_members(group_id INTEGER)
    --RETURNS SETOF group_member_t AS
    --$BODY$
        --SELECT
            --table_member.name AS member_name,
            --table_member_group.is_owner
        --FROM table_member_group
        --INNER JOIN table_member
            --ON table_member_group.member_id = table_member.id
        --WHERE table_member_group.group_id = $1
    --$BODY$
    --LANGUAGE 'sql'
    --SECURITY DEFINER;


-- List the expenses of a group, based on a group name
DROP TYPE IF EXISTS expense_t CASCADE;
CREATE TYPE expense_t AS (
    id INTEGER,
    date_info DATE,
    description VARCHAR,
    amount NUMERIC,
    expense_maker VARCHAR,
    expense_members VARCHAR);
    
CREATE OR REPLACE FUNCTION get_group_expenses(group_id INTEGER)
    RETURNS SETOF expense_t AS
    $BODY$
        SELECT
            table_expense.id,
            table_expense.date_info,
            table_expense.description,
            table_expense.amount,
            expense_maker_name.name AS expense_maker,
            STRING_AGG(expense_members_names.name, '|') AS expense_members
        FROM table_expense
        INNER JOIN table_expense_member expense_members
            ON table_expense.id = expense_members.expense_id
        INNER JOIN table_member expense_members_names
            ON expense_members_names.id = expense_members.member_id
        INNER JOIN table_expense_member expense_maker
            ON table_expense.id = expense_maker.expense_id
                AND expense_maker.made_expense IS TRUE
        INNER JOIN table_member expense_maker_name
            ON expense_maker_name.id = expense_maker.member_id
        WHERE table_expense.group_id = $1
        GROUP BY
            table_expense.id,
            table_expense.date_info,
            table_expense.description,
            table_expense.amount,
            expense_maker_name.name
        ORDER BY table_expense.date_info ASC
    $BODY$
    LANGUAGE 'sql'
    SECURITY DEFINER;


-- List the transfers of a group
DROP TYPE IF EXISTS transfer_t CASCADE;
CREATE TYPE transfer_t AS (
    id INTEGER,
    date_info DATE,
    amount NUMERIC,
    from_member VARCHAR,
    to_member VARCHAR);
    
CREATE OR REPLACE FUNCTION get_group_transfers(group_id INTEGER)
    RETURNS SETOF transfer_t AS
    $BODY$
        SELECT
            table_transfer.id,
            table_transfer.date_info,
            table_transfer.amount,
            from_members_lookup.name,
            to_members_lookup.name
        FROM table_transfer
        INNER JOIN table_member from_members_lookup
            ON from_members_lookup.id = table_transfer.from_member_id
        INNER JOIN table_member to_members_lookup
            ON to_members_lookup.id = table_transfer.to_member_id
        WHERE table_transfer.group_id = $1
        ORDER BY table_transfer.date_info ASC
    $BODY$
    LANGUAGE 'sql'
    SECURITY DEFINER;


-- Get the balance of a given member in a given group
CREATE OR REPLACE FUNCTION get_member_balance(member_name VARCHAR, group_id INTEGER)
    RETURNS NUMERIC AS
    $BODY$
        -- Difference of the amounts to pay and already paid
        SELECT COALESCE(share_to_pay_agg.amount, 0.0)
               - COALESCE(expenses_made_agg.amount, 0.0)
               - COALESCE(transfers_made_agg.amount, 0.0)
               + COALESCE(transfers_received_agg.amount, 0.0)
               AS balance
        FROM (
            -- Aggregation of the total amount of the selected expenses
            -- weighted by the number of members involved in each expense
            SELECT SUM(table_expense.amount / num_members_agg.num_members) AS amount
            FROM (
                -- Count of the number of members in the expenses
                SELECT 
                    table_expense_member.expense_id,
                    COUNT(table_expense_member.member_id) AS num_members
                FROM table_expense_member
                WHERE table_expense_member.expense_id IN (
                    -- Expense IDs matching the member and the group
                    SELECT table_expense.id AS expense_id
                    FROM table_expense
                    INNER JOIN table_expense_member
                        ON table_expense_member.expense_id = table_expense.id
                    INNER JOIN table_member
                        ON table_expense_member.member_id = table_member.id
                    WHERE table_expense.group_id = $2
                        AND table_member.name = $1
                )
                GROUP BY table_expense_member.expense_id
            ) AS num_members_agg
            -- Link to the expense table based on the expenses for which
            -- the number of members was aggregated
            INNER JOIN table_expense
                ON num_members_agg.expense_id = table_expense.id
        ) AS expenses_made_agg,
        (
            -- Expenses matching the member and the group, for which the member actually
            -- made the expense, and aggregation of the total amount
            SELECT SUM(table_expense.amount) AS amount
            FROM table_expense
            INNER JOIN table_expense_member
                ON table_expense_member.expense_id = table_expense.id
            INNER JOIN table_member
                ON table_expense_member.member_id = table_member.id
            WHERE table_expense.group_id = $2
                AND table_member.name = $1
                AND table_expense_member.made_expense IS TRUE
        ) AS share_to_pay_agg,
        (
            -- Transfers matching the member and the group, for which the member received money,
            SELECT SUM(table_transfer.amount) AS amount
            FROM table_transfer
            INNER JOIN table_member
                ON table_transfer.to_member_id = table_member.id
            WHERE table_transfer.group_id = $2
                AND table_member.name = $1
        ) AS transfers_received_agg,
        (
            -- Transfers matching the member and the group, for which the member paid money,
            SELECT SUM(table_transfer.amount) AS amount
            FROM table_transfer
            INNER JOIN table_member
                ON table_transfer.from_member_id = table_member.id
            WHERE table_transfer.group_id = $2
                AND table_member.name = $1
        ) AS transfers_made_agg
    $BODY$
    LANGUAGE 'sql'
    SECURITY DEFINER;
    

-- List the balances of all members of a group
DROP TYPE IF EXISTS group_member_balance_t CASCADE;
CREATE TYPE group_member_balance_t AS (
    name VARCHAR,
    is_owner BOOLEAN,
    balance NUMERIC);
CREATE OR REPLACE FUNCTION get_group_members(group_id INTEGER)
    RETURNS SETOF group_member_balance_t AS
    $BODY$
        DECLARE
            member group_member_balance_t;
        BEGIN
            FOR member IN (
                SELECT
                    table_member.name,
                    table_member_group.is_owner,
                    0.0::NUMERIC
                    
                FROM table_member_group
                INNER JOIN table_member
                    ON table_member_group.member_id = table_member.id
                WHERE table_member_group.group_id = $1
            )
            LOOP
                member.balance = get_member_balance(member.name, $1);
                RETURN NEXT member;
            END LOOP;
            RETURN;
        END
    $BODY$
    LANGUAGE 'plpgsql'
    SECURITY DEFINER;



--
-- SETTER FUNCTIONS
--


-- Create a new group
CREATE OR REPLACE FUNCTION insert_member(member_name VARCHAR,
                                         member_password_hash VARCHAR,
                                         member_password_salt VARCHAR)
    RETURNS VOID AS
    $BODY$
        DECLARE
            member_id INTEGER;
        BEGIN
            INSERT INTO table_member (name, password_hash, password_salt)
                VALUES ($1, DECODE($2, 'base64'), DECODE($3, 'base64'));
            member_id := (SELECT currval(pg_get_serial_sequence('table_member', 'id')));
        END
    $BODY$
    LANGUAGE 'plpgsql'
    SECURITY DEFINER;
    
    
-- Create a new group
CREATE OR REPLACE FUNCTION insert_group(name VARCHAR,
                                        owner_name VARCHAR,
                                        other_members VARIADIC VARCHAR[])
    RETURNS INTEGER AS
    $BODY$
        DECLARE
            group_id INTEGER;
            other_member_name VARCHAR;
            new_member_id INTEGER;
        BEGIN
            INSERT INTO table_group (name)
                VALUES ($1);
            group_id := (SELECT currval(pg_get_serial_sequence('table_group', 'id')));
            new_member_id := (SELECT table_member.id FROM table_member WHERE table_member.name = $2);
            INSERT INTO table_member_group (member_id, group_id, is_owner)
                VALUES (new_member_id, group_id, TRUE);
            FOR other_member_name IN (SELECT i FROM UNNEST($3) AS i )
            LOOP
                new_member_id := (SELECT table_member.id FROM table_member WHERE table_member.name = other_member_name);
                INSERT INTO table_member_group (member_id, group_id, is_owner)
                    VALUES (new_member_id, group_id, FALSE);
            END LOOP;
            RETURN group_id;
        END
    $BODY$
    LANGUAGE 'plpgsql'
    SECURITY DEFINER;
    
    
-- Create a new group member
CREATE OR REPLACE FUNCTION insert_group_member(new_member_name VARCHAR,
                                               target_group_id INTEGER)
    RETURNS VOID AS
    $BODY$
        DECLARE
            new_member_id INTEGER;
        BEGIN
            new_member_id := (SELECT table_member.id FROM table_member WHERE table_member.name = $1);
            INSERT INTO table_member_group (member_id, group_id, is_owner)
                VALUES (new_member_id, $2, FALSE);
        END
    $BODY$
    LANGUAGE 'plpgsql'
    SECURITY DEFINER;
    

CREATE OR REPLACE FUNCTION insert_expense(date_info DATE,
                                          description VARCHAR,
                                          amount NUMERIC,
                                          target_group_id INTEGER,
                                          maker_name VARCHAR,
                                          other_members_name VARIADIC VARCHAR[])
    RETURNS INTEGER AS
    $BODY$
        DECLARE
            new_expense_id INTEGER;
            new_member_id INTEGER;
            maker_id INTEGER;
            other_member_name VARCHAR;
        BEGIN
            INSERT INTO table_expense (date_info, description, amount, group_id)
                VALUES ($1, $2, $3, $4);
            new_expense_id := (SELECT currval(pg_get_serial_sequence('table_expense', 'id')));
            new_member_id := (SELECT id FROM table_member WHERE table_member.name = $5);
            INSERT INTO table_expense_member (expense_id, member_id, made_expense)
                VALUES (new_expense_id, new_member_id, TRUE);
            FOR other_member_name IN (SELECT i FROM UNNEST($6) AS i )
            LOOP
                new_member_id := (SELECT id FROM table_member WHERE table_member.name = other_member_name);
                INSERT INTO table_expense_member (expense_id, member_id, made_expense)
                    VALUES (new_expense_id, new_member_id, FALSE);
            END LOOP;
            RETURN new_expense_id;
        END
    $BODY$
    LANGUAGE 'plpgsql'
    SECURITY DEFINER;


CREATE OR REPLACE FUNCTION insert_transfer(date_info DATE,
                                           amount NUMERIC,
                                           target_group_id INTEGER,
                                           from_member_name VARCHAR,
                                           to_member_name VARCHAR)
    RETURNS INTEGER AS
    $BODY$
        DECLARE
            member_id_1 INTEGER;
            member_id_2 INTEGER;
            new_transfer_id INTEGER;
        BEGIN
            member_id_1 := (SELECT id FROM table_member WHERE table_member.name = $4);
            member_id_2 := (SELECT id FROM table_member WHERE table_member.name = $5);
            INSERT INTO table_transfer (date_info, amount, group_id, from_member_id, to_member_id)
                VALUES ($1, $2, $3, member_id_1, member_id_2);
            new_transfer_id := (SELECT currval(pg_get_serial_sequence('table_transfer', 'id')));
            RETURN new_transfer_id;
        END
    $BODY$
    LANGUAGE 'plpgsql'
    SECURITY DEFINER;


-- Remove an expense
CREATE OR REPLACE FUNCTION delete_expense(expense_id INTEGER)
    RETURNS VOID AS
    $BODY$
        DELETE FROM table_expense WHERE id=$1;
    $BODY$
    LANGUAGE 'sql'
    SECURITY DEFINER;


-- Remove a transfer
CREATE OR REPLACE FUNCTION delete_transfer(transfer_id INTEGER)
    RETURNS VOID AS
    $BODY$
        DELETE FROM table_transfer WHERE id=$1;
    $BODY$
    LANGUAGE 'sql'
    SECURITY DEFINER;

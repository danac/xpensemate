--
-- DATABASE STRUCTURE
--
 
 
CREATE TABLE table_member (
    id SERIAL
        PRIMARY KEY, 
    name VARCHAR(15)
        NOT NULL
        UNIQUE
);

 
CREATE TABLE table_group (
    id SERIAL
        PRIMARY KEY, 
    name VARCHAR(50)
        NOT NULL
);

 
CREATE TABLE table_member_group (
    member_id INTEGER
        NOT NULL
        REFERENCES table_member (id),
    group_id INTEGER
        NOT NULL
        REFERENCES table_group (id),
    PRIMARY KEY (member_id, group_id)
);

 
CREATE TABLE table_expense (
    id SERIAL
        PRIMARY KEY, 
    date DATE
        NOT NULL, 
    description TEXT
        NOT NULL, 
    amount NUMERIC
        NOT NULL,
    group_id INTEGER
        NOT NULL
        REFERENCES table_group (id)
);

 
CREATE TABLE table_expense_member (
    expense_id INTEGER
        NOT NULL
        REFERENCES table_expense (id),
    member_id INTEGER
        NOT NULL
        REFERENCES table_member (id),
    made_expense boolean
        NOT NULL,
    PRIMARY KEY (expense_id, member_id)
);



--
-- TRIGGER FUNCTIONS
--

CREATE FUNCTION check_expense_member_group_func()
  RETURNS TRIGGER AS
$BODY$
DECLARE
    num_rows INTEGER;
BEGIN
    num_rows := (
        SELECT COUNT(*)
        FROM table_member_group
        INNER JOIN table_expense ON table_expense.id = NEW.expense_id
        WHERE table_member_group.group_id = table_expense.group_id
        AND table_member_group.member_id = NEW.member_id
    );
                
    IF num_rows = 1 THEN
      RETURN NEW;
    ELSE 
      RAISE EXCEPTION 'User not in expense group';
    END IF;
END;
$BODY$
LANGUAGE 'plpgsql';


CREATE FUNCTION check_expense_maker_func()
    RETURNS TRIGGER AS
    $BODY$
        DECLARE
            num_makers INTEGER;
        BEGIN
            IF NEW.made_expense = FALSE THEN
                RETURN NEW;
            END IF;
            num_makers := (
                SELECT COUNT(*)
                FROM table_expense_member
                WHERE table_expense_member.expense_id = NEW.expense_id
                AND table_expense_member.made_expense = TRUE
            );
                        
            IF num_makers = 0 THEN
                RETURN NEW;
            ELSE 
                RAISE EXCEPTION 'Expense maker already defined';
            END IF;
        END;
    $BODY$
    LANGUAGE 'plpgsql';


--
-- TRIGGER DEFINITIONS
--

CREATE TRIGGER check_expense_member_group
    BEFORE INSERT OR UPDATE ON table_expense_member 
    FOR EACH ROW EXECUTE PROCEDURE check_expense_member_group_func();

CREATE TRIGGER check_expense_maker
    BEFORE INSERT OR UPDATE ON table_expense_member 
    FOR EACH ROW EXECUTE PROCEDURE check_expense_maker_func();


--
-- FUNCTIONS
--

CREATE FUNCTION member_balance_func(member_id INTEGER, group_id INTEGER)
    RETURNS NUMERIC AS
    $BODY$
        SELECT SUM(table_expense.amount / members_agg.num_members) AS balance
        FROM (
            SELECT table_expense_member.expense_id, COUNT(table_expense_member.member_id) AS num_members
            FROM table_expense_member
            WHERE table_expense_member.expense_id IN (
                SELECT table_expense.id AS expense_id
                FROM table_expense
                INNER JOIN table_expense_member ON table_expense_member.expense_id = table_expense.id
                WHERE table_expense.group_id = $2 AND table_expense_member.member_id = $1
            )
            GROUP BY table_expense_member.expense_id
        ) AS members_agg
        INNER JOIN table_expense ON members_agg.expense_id = table_expense.id;
    $BODY$
    LANGUAGE 'sql';
    
    
CREATE TYPE member_balance AS (member_id INTEGER, balance numeric);
CREATE OR REPLACE FUNCTION group_balance_func(group_id INTEGER)
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
                result_row.balance = member_balance_func(member_id, $1);
                RETURN NEXT result_row;
            END LOOP;
            RETURN;
        END
    $BODY$
    LANGUAGE 'plpgsql';




--
-- VIEWS
--


CREATE VIEW view_expense_with_member_names AS
    SELECT table_expense.*, expense_member_agg.expense_members
    FROM (
        SELECT table_expense_member.expense_id, string_agg(table_member.name, '|') AS expense_members
        FROM table_expense_member
        INNER JOIN table_member ON table_member.id = table_expense_member.member_id
        GROUP BY table_expense_member.expense_id)
    AS expense_member_agg
    INNER JOIN table_expense ON expense_member_agg.expense_id = table_expense.id;

CREATE VIEW view_expense_num_members AS
    SELECT table_expense_member.expense_id, COUNT(table_expense_member.member_id) AS num_members
    FROM table_expense_member
    GROUP BY table_expense_member.expense_id;

CREATE VIEW view_expense_shared_amount AS
    SELECT table_expense.id AS expense_id,
           table_expense.group_id,
           members_agg.num_members,
           table_expense.amount,
           table_expense.amount / members_agg.num_members AS shared_amount
    FROM (
        SELECT table_expense_member.expense_id, COUNT(table_expense_member.member_id) AS num_members
        FROM table_expense_member
        ---WHERE table_expense_member.expense_id IN (SELECT table_expense.id FROM table_expense WHERE table_expense.group_id = 1)
        GROUP BY table_expense_member.expense_id
    ) AS members_agg
    INNER JOIN table_expense ON members_agg.expense_id = table_expense.id;

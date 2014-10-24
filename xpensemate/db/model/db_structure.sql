--
-- DATABASE STRUCTURE
--
 
DROP TABLE IF EXISTS table_member CASCADE;
CREATE TABLE table_member (
    id SERIAL
        PRIMARY KEY, 
    name VARCHAR(15)
        NOT NULL
        UNIQUE,
    password_hash BYTEA
        NOT NULL,
    password_salt BYTEA
        NOT NULL,
    active BOOLEAN
        NOT NULL
        DEFAULT TRUE
);

DROP TABLE IF EXISTS table_group CASCADE;
CREATE TABLE table_group (
    id SERIAL
        PRIMARY KEY, 
    name VARCHAR(50)
        NOT NULL
);


DROP TABLE IF EXISTS table_member_group CASCADE;
CREATE TABLE table_member_group (
    member_id INTEGER
        NOT NULL
        REFERENCES table_member (id),
    group_id INTEGER
        NOT NULL
        REFERENCES table_group (id),
    is_owner BOOLEAN
        NOT NULL,
    PRIMARY KEY (member_id, group_id)
);


DROP TABLE IF EXISTS table_expense CASCADE;
CREATE TABLE table_expense (
    id SERIAL
        PRIMARY KEY, 
    date_info DATE
        NOT NULL, 
    description TEXT
        NOT NULL, 
    amount NUMERIC
        NOT NULL,
    group_id INTEGER
        NOT NULL
        REFERENCES table_group (id)
);

 
DROP TABLE IF EXISTS table_expense_member CASCADE;
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

--
-- DATABASE STRUCTURE
--
 
 
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

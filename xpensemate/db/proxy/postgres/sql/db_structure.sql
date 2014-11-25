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
-- DATABASE STRUCTURE
--
 
DROP TABLE IF EXISTS table_member CASCADE;
CREATE TABLE table_member (
    id SERIAL
        PRIMARY KEY,
    name VARCHAR(15)
        NOT NULL
        UNIQUE,
    password TEXT
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
        NOT NULL,
    smallest_unit NUMERIC
        NOT NULL
);


DROP TABLE IF EXISTS table_member_group CASCADE;
CREATE TABLE table_member_group (
    member_id INTEGER
        NOT NULL
        REFERENCES table_member (id),
    group_id INTEGER
        NOT NULL
        REFERENCES table_group (id)
        ON DELETE CASCADE,
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
        ON DELETE CASCADE
);

 
DROP TABLE IF EXISTS table_expense_member CASCADE;
CREATE TABLE table_expense_member (
    expense_id INTEGER
        NOT NULL
        REFERENCES table_expense (id)
        ON DELETE CASCADE,
    member_id INTEGER
        NOT NULL
        REFERENCES table_member (id),
    made_expense boolean
        NOT NULL,
    PRIMARY KEY (expense_id, member_id)
);
 
 
DROP TABLE IF EXISTS table_transfer CASCADE;
CREATE TABLE table_transfer (
    id SERIAL
        PRIMARY KEY,
    date_info DATE
        NOT NULL,
    amount NUMERIC
        NOT NULL,
    from_member_id INTEGER
        NOT NULL
        REFERENCES table_member (id),
    to_member_id INTEGER
        NOT NULL
        REFERENCES table_member (id),
    group_id INTEGER
        NOT NULL
        REFERENCES table_group (id)
        ON DELETE CASCADE
);

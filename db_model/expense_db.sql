 
--
-- DATABASE STRUCTURE
--
 
 
CREATE TABLE "member" (
    "id" serial
        PRIMARY KEY , 
    "name" varchar(15)
        NOT NULL
        UNIQUE
);

 
CREATE TABLE "group" (
    "id" serial
        PRIMARY KEY , 
    "name" varchar(50)
        NOT NULL
);

 
CREATE TABLE "member_group" (
    "member_id" integer
        NOT NULL
        REFERENCES "member" ( "id" ) ,
    "group_id" integer
        NOT NULL
        REFERENCES "group" ( "id" ) ,
    PRIMARY KEY ("member_id", "group_id")
);

 
CREATE TABLE "expense" (
    "id" serial
        PRIMARY KEY , 
    "date" date
        NOT NULL , 
    "description" text
        NOT NULL , 
    "amount" money
        NOT NULL ,
    "group_id" integer
        NOT NULL
        REFERENCES "group" ( "id" )
);

 
CREATE TABLE "expense_member" (
    "expense_id" integer
        NOT NULL
        REFERENCES "expense" ( "id" ) ,
    "member_id" integer
        NOT NULL
        REFERENCES "member" ( "id" ) , 
    "group_id" integer
        NOT NULL
        REFERENCES "member" ( "id" ) , 
    "made_expense" boolean
        NOT NULL ,
    PRIMARY KEY ( "expense_id" , "member_id" )
);



--
-- FUNCTIONS
--

CREATE FUNCTION check_expense_member_group_func()
  RETURNS trigger AS
$BODY$
DECLARE
    num_rows integer;
BEGIN
    num_rows := (
        SELECT COUNT(*)
        FROM "member_group"
        INNER JOIN "expense" ON "expense"."id" = NEW."expense_id"
        WHERE "member_group"."group_id" = "expense"."group_id"
        AND "member_group"."member_id" = NEW."member_id"
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
    RETURNS trigger AS
    $BODY$
        DECLARE
            num_makers integer;
        BEGIN
            IF NEW."made_expense" = FALSE THEN
                RETURN NEW;
            END IF;
            num_makers := (
                SELECT COUNT(*)
                FROM "expense_member"
                WHERE "expense_member"."expense_id" = NEW.expense_id
                AND "expense_member"."made_expense" = TRUE
            );
                        
            IF num_makers = 0 THEN
                RETURN NEW;
            ELSE 
                RAISE EXCEPTION 'Expense maker already defined';
            END IF;
        END;
    $BODY$
    LANGUAGE 'plpgsql';


CREATE TYPE member_balance as (member_id integer, group_id int8);
CREATE FUNCTION check_expense_maker_func()
    RETURNS setof  AS
    $BODY$
        DECLARE

        BEGIN

        END;
    $BODY$
    LANGUAGE 'plpgsql';



--
-- TRIGGER DEFINITIONS
--

CREATE TRIGGER check_expense_member_group
    BEFORE INSERT OR UPDATE ON "expense_member" 
    FOR EACH ROW EXECUTE PROCEDURE check_expense_member_group_func();

CREATE TRIGGER check_expense_maker
    BEFORE INSERT OR UPDATE ON "expense_member" 
    FOR EACH ROW EXECUTE PROCEDURE check_expense_maker_func();


--
-- VIEWS
--

CREATE VIEW "view_expense_with_member_names" AS
    SELECT "expense".*, "expense_member_agg"."expense_members"
    FROM (
        SELECT "expense_member"."expense_id", string_agg("member"."name", '|') AS "expense_members"
        FROM "expense_member"
        INNER JOIN "member" ON "member"."id" = "expense_member"."member_id"
        GROUP BY "expense_member"."expense_id")
    AS "expense_member_agg"
    INNER JOIN "expense" ON "expense_member_agg"."expense_id" = "expense"."id";

CREATE VIEW "view_expense_num_members" AS
    SELECT "expense_member"."expense_id", COUNT("expense_member"."member_id") AS "num_members"
    FROM "expense_member"
    GROUP BY "expense_member"."expense_id";

CREATE VIEW "view_expense_shared_amount" AS
    SELECT "expense"."id" AS "expense_id",
           "expense"."group_id",
           "members_agg"."num_members",
           "expense"."amount",
           "expense"."amount" / "members_agg"."num_members" AS "shared_amount"
    FROM (
        SELECT "expense_member"."expense_id", COUNT("expense_member"."member_id") AS "num_members"
        FROM "expense_member"
        ---WHERE "expense_member"."expense_id" IN (SELECT "expense"."id" FROM "expense" WHERE "expense"."group_id" = 1)
        GROUP BY "expense_member"."expense_id"
    ) AS "members_agg"
    INNER JOIN "expense" ON "members_agg"."expense_id" = "expense"."id";

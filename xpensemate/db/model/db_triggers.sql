
--
-- TRIGGER FUNCTIONS
--

CREATE OR REPLACE FUNCTION check_expense_member_group()
  RETURNS TRIGGER AS
$BODY$
DECLARE
    member_exists BOOLEAN;
BEGIN
    member_exists := (
        SELECT EXISTS (
            SELECT *
            FROM table_member_group
            INNER JOIN table_expense ON table_expense.id = NEW.expense_id
            WHERE table_member_group.group_id = table_expense.group_id
                AND table_member_group.member_id = NEW.member_id
        )
    );
                
    IF member_exists IS TRUE THEN
      RETURN NEW;
    ELSE 
      RAISE EXCEPTION 'Member not in expense group';
    END IF;
END;
$BODY$
LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION check_expense_maker()
    RETURNS TRIGGER AS
    $BODY$
        DECLARE
            num_makers INTEGER;
            num_members INTEGER;
        BEGIN
            num_members := (
                SELECT COUNT(*)
                FROM table_expense_member
                WHERE table_expense_member.expense_id = NEW.expense_id
            );
            num_makers := (
                SELECT COUNT(*)
                FROM table_expense_member
                WHERE table_expense_member.expense_id = NEW.expense_id
                    AND table_expense_member.made_expense = TRUE
            );
                        
            IF NEW.made_expense IS FALSE AND num_members = 0 THEN
                RAISE EXCEPTION 'First member of an expense must have made it';
            END IF;
            
            IF NEW.made_expense IS TRUE and num_makers > 0 THEN
                RAISE EXCEPTION 'Expense maker already defined';
            END IF;
            
            RETURN NEW;
        END;
    $BODY$
    LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION check_group_owner()
    RETURNS TRIGGER AS
    $BODY$
        DECLARE
            num_owners INTEGER;
            num_members INTEGER;
        BEGIN
            num_members := (
                SELECT COUNT(*)
                FROM table_member_group
                WHERE table_member_group.group_id = NEW.group_id
            );
            num_owners := (
                SELECT COUNT(*)
                FROM table_member_group
                WHERE table_member_group.group_id = NEW.group_id
                    AND table_member_group.is_owner = TRUE
            );
                  
            IF NEW.is_owner IS FALSE AND num_members = 0 THEN
                RAISE EXCEPTION 'First member of a group must be owner';
            END IF;
            
            IF NEW.is_owner IS TRUE and num_owners > 0 THEN
                RAISE EXCEPTION 'Group already owned';
            END IF;
            
            RETURN NEW;
        END;
    $BODY$
    LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION check_transfer_member_group()
  RETURNS TRIGGER AS
$BODY$
DECLARE
    from_member_exists BOOLEAN;
    to_member_exists BOOLEAN;
BEGIN
    from_member_exists := (
        SELECT EXISTS (
            SELECT *
            FROM table_member_group
            WHERE table_member_group.group_id = NEW.group_id
                AND table_member_group.member_id = NEW.from_member_id
        )
    );
    to_member_exists := (
        SELECT EXISTS (
            SELECT *
            FROM table_member_group
            WHERE table_member_group.group_id = NEW.group_id
                AND table_member_group.member_id = NEW.to_member_id
        )
    );
                
    IF from_member_exists IS TRUE AND to_member_exists IS TRUE THEN
      RETURN NEW;
    ELSE 
      RAISE EXCEPTION 'Members of the transfer are not both in transfer group';
    END IF;
END;
$BODY$
LANGUAGE 'plpgsql';

--
-- TRIGGER DEFINITIONS
--

DROP TRIGGER IF EXISTS check_expense_member_group ON table_expense_member;
CREATE TRIGGER check_expense_member_group
    BEFORE INSERT OR UPDATE
    ON table_expense_member 
    FOR EACH ROW
    EXECUTE PROCEDURE check_expense_member_group();

DROP TRIGGER IF EXISTS check_expense_maker ON table_expense_member;
CREATE TRIGGER check_expense_maker
    BEFORE INSERT OR UPDATE
    ON table_expense_member 
    FOR EACH ROW
    EXECUTE PROCEDURE check_expense_maker();

DROP TRIGGER IF EXISTS check_group_owner ON table_member_group;
CREATE TRIGGER check_group_owner
    BEFORE INSERT OR UPDATE
    ON table_member_group 
    FOR EACH ROW
    EXECUTE PROCEDURE check_group_owner();
DROP TRIGGER IF EXISTS check_expense_member_group ON table_expense_member;

CREATE TRIGGER check_transfer_member_group
    BEFORE INSERT OR UPDATE
    ON table_transfer
    FOR EACH ROW
    EXECUTE PROCEDURE check_transfer_member_group();

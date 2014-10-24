
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

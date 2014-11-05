*********************
Database architecture
*********************

A few words about the database


Tables and relations
====================

.. image:: /static/db_relations.png

==================== ===========
Tables               Description
==================== ===========
table_member         Contains information relevent to users
table_group          Holds the various groups of members
table_member_group   Links members to groups (many-to-many relationship)
table_expense        Contains all expenses
table_expense_member Links expenses to members (many-to-many relationship)
table_transfer	     Contains all money transfers between members
==================== ===========



Constraints
===========

Besides the uniqueness and foreign key constraints inherent to the table definitions,
a few triggers are defined to ensure the following points:

* the members linked to expenses and transfers belong to the group of the expense/transfer
* an expense has one and only maker
* a group has one and only one owner


.. _db_stored_functions:

Stored functions
================

A collection of stored functions implement an interface to the contents of
the database.

**This should be the only entry point into the database in the Python code**,
since it makes data access independent from the underlying tables and views.


Getters
+++++++

.. py:function:: get_member(name VARCHAR)

    Returns details about a user

    :return:
        * name VARCHAR
        * password_hash VARCHAR
        * password_salt VARCHAR
        * active BOOLEAN


.. C:function:: get_member_groups(member_name VARCHAR)

    Returns the groups a user belongs to.

    :return:
        * id INTEGER
        * name VARCHAR
       
       
.. C:function:: get_group(group_id INTEGER)

    Returns the details of the group

    :return:
        * id INTEGER
        * name VARCHAR
       
       
.. C:function:: get_group_members(group_id INTEGER)

    Returns the members of a group, with their respective balances in the group.

    :return:
        * name VARCHAR
        * is_owner BOOLEAN
        * balance NUMERIC
       
       
.. C:function:: get_group_expenses(group_id INTEGER)

    Returns the expenses of a group, chronologically ordered.
    The result set includes a cncatenated list of all members concerned by the
    expense, separated by the ``|`` character.

    :return:
        * id INTEGER
        * date_info DATE
        * description VARCHAR
        * amount NUMERIC
        * expense_maker VARCHAR
        * expense_members VARCHAR

       
.. C:function:: get_group_transfers(group_id INTEGER)

    Returns the transfers (i.e. reimbursements) in a group, chronologically ordered.

    :return:
        * id INTEGER
        * date_info DATE
        * description VARCHAR
        * amount NUMERIC
        * from_member VARCHAR
        * to_member VARCHAR

       
.. C:function:: get_member_balance(member_name VARCHAR, group_id INTEGER)

    Returns the balance of a member in a given group. 
    This corresponds to the amount of money owed to the other group members
    if positive, or the amount of money to receive from the other members if
    negative.

    :rtype: NUMERIC


Setters
+++++++

.. C:function:: insert_member(member_name VARCHAR, member_password_hash VARCHAR, member_password_salt VARCHAR)

    Creates a new user.

    :return: Nothing


.. C:function:: insert_group(name VARCHAR, owner_name VARCHAR, other_members VARIADIC VARCHAR[])

    Creates a new group.

    :return: The ID of the newly created group
    :rtype: INTEGER


.. C:function:: insert_group_member(new_member_name VARCHAR, target_group_id INTEGER)

    Adds an existing user to a group.

    :return: Nothing
    
    
.. C:function:: insert_expense(date_info DATE, description VARCHAR, amount NUMERIC, target_group_id INTEGER, maker_name VARCHAR, other_members_name VARIADIC VARCHAR[])

    Adds an expense in a group.

    :return: The ID of the newly inserted expense.
    :rtype: INTEGER
    
    
.. C:function:: insert_transfer(date_info DATE, amount NUMERIC, target_group_id INTEGER, from_member_name VARCHAR, to_member_name VARCHAR)

    Adds a transfer in a group.

    :return: The ID of the newly inserted transfer.
    :rtype: INTEGER
    

.. C:function:: delete_expense(expense_id INTEGER)

    Deletes an expense.

    :return: Nothing
    

.. C:function:: delete_transfer(transfer_id INTEGER)

    Deletes a transfer.

    :return: Nothing


.. SQL source code
.. ===============

.. Table definitions
.. +++++++++++++++++

.. .. literalinclude:: ../../xpensemate/db/model-postgres/db_structure.sql


.. Triggers
.. ++++++++

.. .. literalinclude:: ../../xpensemate/db/model-postgres/db_triggers.sql


.. Stored procedures
.. +++++++++++++++++

.. .. literalinclude:: ../../xpensemate/db/model-postgres/db_functions.sql

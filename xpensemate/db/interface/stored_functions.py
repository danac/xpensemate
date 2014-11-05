#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Dana Christen
#
# This file is part of XpenseMate, a tool for managing shared expenses and
# hosted at https://github.com/danac/xpensemate.
#
# XpenseMate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from xpensemate.data_types import MemberWithCredentials, Group, GroupWithExpenses, Expense, Transfer
from xpensemate.db.interface.abstract_interface import AbstractDatabaseInterface
from xpensemate.db.proxy import DatabaseProxyFactory


class StoredFunctionsDatabaseInterface(AbstractDatabaseInterface):
    """
    This class implements an interface to databases
    exposing the stored procedures described in :ref:`db_stored_functions`.
    """
    
    def __init__(self):
        
        #: Database proxy, implementing :class:`xpensemate.db.proxy.AbstractDatabaseProxy`
        self.db_proxy = DatabaseProxyFactory.get_proxy()
        
        
    def get_member_credentials(self, member_name):
        rows = []
        for i in self._execute_stored_procedure("get_member", member_name):
            rows.append(i)
        assert len(rows) == 1, "Found duplicate member names!"
        s=rows[0]
        result = MemberWithCredentials(
            name = s[0],
            password_hash = s[1],
            password_salt = s[2],
            hash_function = DBConfig.password_hashing_function,
            active = s[3])
        
        return result
        
        
    def get_member_groups(self, member_name):
        for group in self._execute_stored_procedure("get_groups", member_name):
            yield self._instantiate_group(group[0])
    

    def get_group_with_movements(self, group_id):
        group = self._instantiate_group(group_id)
        
        expenses = []
        for row in self._execute_stored_procedure("get_group_expenses", group_id):
            typed_expense = Expense(
                expense_id = row[0],
                description = row[1],
                date = row[2],
                amount = row[3],
                maker = row[4],
                members = row[5].split(DBConfig.string_concat_delimiter))
            expenses.append(typed_expense)
        
        transfers = []
        for row in self._execute_stored_procedure("get_group_transfers", group_id):
            typed_transfer = Transfer(
                transfer_id = row[0],
                date = row[1],
                amount = row[2],
                from_member = row[3],
                to_member = row[4])
            transfers.append(typed_transfer)
    
        return GroupWithExpenses(expenses=expenses, transfers=transfers, **group.__dict__)
        
        
    def _instantiate_group(self, group_id):
        balances = dict(zip(*zip(*self._execute_stored_procedure("get_group_balances", group_id))))
        typed_group = Group(
            group_id=group_id,
            name=group_name,
            member_balances = balances) 
        return typed_group
    
    
    def _execute_stored_procedure(self, procedure_name, *args):
        def quote_strings(arg):
            if type(arg) is str:
                return "'{}'".format(arg)
            else:
                return str(arg)
        quoted_args = map(quote_strings, args)
        
        sql_query = "SELECT * FROM {}({});".format(procedure_name, ', '.join(quoted_args))
        
        return self.db_proxy.query(sql_query)

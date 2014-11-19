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
from xpensemate.db.proxy.factory import DatabaseProxyFactory
from xpensemate.config import DBConfig
from xpensemate.utils.benchmark import timeit


class StoredFunctionsDatabaseInterface(AbstractDatabaseInterface):
    """
    This class implements an interface to databases
    exposing the stored procedures described in :ref:`db_stored_functions`.
    """
    
    def __init__(self, db_proxy=None):
        
        #: Database proxy, implementing :class:`AbstractDatabaseProxy <xpensemate.db.proxy.abstract_proxy.AbstractDatabaseProxy>`
        self.db_proxy = db_proxy
        
        if self.db_proxy is None:
            self.db_proxy = DatabaseProxyFactory.get_proxy()

    @timeit
    def get_member_credentials(self, member_name):
        rows = []
        for i in self._execute_stored_procedure("get_member", member_name):
            rows.append(i)
        assert len(rows) == 1, "Did not find unique member name!"
        s=rows[0]
        result = MemberWithCredentials(
            name = s[0],
            password = s[1],
            active = s[2])
        
        return result
        
    @timeit
    def get_member_groups(self, member_name):
        results = self._execute_stored_procedure("get_member_groups", member_name)
        return [self._instantiate_group(*group) for group in results]
    
    @timeit
    def get_group_with_movements(self, group_id):
        group = self._instantiate_group(group_id)
        
        expenses = []
        for row in self._execute_stored_procedure("get_group_expenses", group_id):
            typed_expense = Expense(
                expense_id = row[0],
                date = row[1],
                description = row[2],
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
        
        
    def insert_group(self, group):
        arguments = [group.name, group.smallest_unit, group.owner]
        arguments += group.member_balance
        self._execute_stored_procedure("insert_group", *arguments)
        
        
    def insert_member(self, member):
        arguments = member.name, member.password
        self._execute_stored_procedure("insert_member", *arguments)
        
        
    def insert_group_member(self, member_name, group_id):
        arguments = member_name, group_id
        self._execute_stored_procedure("insert_group_member", *arguments)
        
        
    def insert_expense(self, expense, group_id):
        other_members = [m for m in expense.members if m != expense.maker]
        arguments = [expense.date,
                    expense.description,
                    expense.amount,
                    group_id,
                    expense.maker]
        arguments += other_members
        self._execute_stored_procedure("insert_expense", *arguments)
                    
        
    def insert_transfer(self, transfer, group_id):
        arguments = [transfer.date,
                     transfer.amount,
                     group_id,
                     transfer.from_member,
                     transfer.to_member]
        self._execute_stored_procedure("insert_transfer", *arguments)
        
    
    def delete_expense(self, expense_id):
        self._execute_stored_procedure("delete_expense", expense_id)
        
    
    def delete_transfer(self, transfer_id):
        self._execute_stored_procedure("delete_transfer", transfer_id)
        
        
    def _instantiate_group(self, group_id, group_name=None):
        if group_name is None:
            group_details = self._execute_stored_procedure("get_group", group_id)
            group_name = group_details[0][1]
            smallest_unit = group_details[0][2]
            
        result_set = self._execute_stored_procedure("get_group_members", group_id)
        
        # The DB returns a table whose columns are (member name, is owner, balance
        columns = list(zip(*result_set))
        
        balances = dict(zip(columns[0], columns[2]))
        
        owner_index = columns[1].index(True)
        owner = columns[owner_index]
        
        typed_group = Group(
            group_id=group_id,
            name=group_name,
            smallest_unit=smallest_unit,
            owner=owner,
            member_balance = balances)
            
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

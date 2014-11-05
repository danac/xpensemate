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

import abc
from xpensemate.config import DBConfig
from xpensemate.db.proxy import DatabaseProxyFactory
from xpensemate.data_types import MemberWithCredentials, Group, GroupWithExpenses, Expense, Transfer


class AbstractDatabaseInterface(metaclass=abc.ABCMeta):
    """
    This abstract class describes the interface to the storage
    backend.
    """
    
    @abc.abstractmethod
    def get_member_credentials(self, member_name):
        """
        Returns the details of a user.
     
        :param str member_name: The name of the user.
     
        :return: A :class:`xpensemate.data_types.MemberWithCredentials` instance.
        """
        pass
    
    
    @abc.abstractmethod
    def get_member_groups(self, member_name):
        """
        Returns the groups a user belongs to.
     
        :param str member_name: The name of the user.
     
        :return: An iterable over :class:`xpensemate.data_types.Group` intances.
        """
        pass
    
    
    @abc.abstractmethod
    def get_group_with_movements(self, group_id):
        """
        Returns the expenses of a group.
     
        :param int group_id: The id number of the group.
     
        :return: A :class:`xpensemate.data_types.GroupWithExpenses` instance.
        """
        pass


class StoredFunctionsInterface():
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

    
class DatabaseInterfaceFactory:
    """
    Factory class used to automatically instantiate a database factory
    based on the type of interface defined in :class:`xpensemate.config.DBConfig`.
    """
    
    #: Singleton instance of the database interface
    db_interface_instance = None
    
    #: Dictionary mapping the possible interface types in
    #: :data:`xpensemate.config.DBConfig.interface` to classes
    interface_class_dispatch = {
        "stored_functions" : StoredFunctionsInterface
    }
    
    
    @classmethod
    def get_interface(cls):
        """
        Returns the unique database proxy, after instantiating it
        if necessary
        
        :return: The singleton instance to the database proxy
        """
        
        if cls.db_interface_instance is None:
            cls._instantiate_interface_instance()
        
        return cls.db_interface_instance
        
        
    @classmethod
    def _instantiate_interface_instance(cls):
        interface_type = DBConfig.interface
        try:
            interface_class = cls.interface_class_dispatch[interface_type]()
            cls.db_interface_instance = interface_class
            
        except KeyError:
            message = "Database interface not implemented: {}".format(interface_type)
            raise NotImplementedError(message)
        
    

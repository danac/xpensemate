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


class AbstractDatabaseInterface(metaclass=abc.ABCMeta):
    """
    This abstract class describes the interface to the storage
    backend.
    """
    
    @abc.abstractmethod
    def get_member_credentials(member_name):
        """
        Returns the details of a user.
     
        :param str member_name: The name of the user.
     
        :return: A :class:`xpensemate.data_types.MemberWithCredentials` instance.
        """
        pass
    
    
    @abc.abstractmethod
    def get_groups(member_id):
        """
        Returns the groups a user belongs to.
     
        :param int member_id: The id number of the user.
     
        :return: An iterable over :class:`xpensemate.data_types.Group` intances.
        """
        pass
    
    
    @abc.abstractmethod
    def get_group_expenses(group_id):
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
        
        
    def get_member_credentials(member_name):
        self.db_proxy.query("")
    
    def _execute_stored_procedure(self, procedure_name, *args):
        sql_query = "SELECT * FROM {}('{}');".format(procedure_name, ', '.join(args))
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
            raise NotImplemented(message)
        
    

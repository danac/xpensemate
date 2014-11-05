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
        
        
    @abc.abstractmethod
    def insert_member(self, member):
        """
        Inserts a new member.
     
        :param member: The member to insert
        :type member: :class:`MemberWithCredentials <xpensemate.data_types.MemberWithCredentials>`
        :return: Nothing
        """
        pass
        
        
    @abc.abstractmethod
    def insert_group(self, group):
        """
        Inserts a new member.
     
        :param group: The group to insert.
        :type group: :class:`Group <xpensemate.data_types.Group>`
        :return: Nothing
        
        .. Note:: The following happens with the argument:
            
            * the :data:`group_id <xpensemate.data_types.Group.group_id>` attribute
              is ignored.
                
            * The keys in the :data:`member_balances <xpensemate.data_types.Group.member_balances>`
              atribute are used to determine the group members. The values are ignored.
              
            * The :data:`maker <xpensemate.data_types.Group.maker>` attribute is used to
              determine the group owner.
            
        """
        pass
        
        
    @abc.abstractmethod
    def insert_group_member(self, member_name, group_id):
        """
        Adds a member to an existing group.
     
        :param str member_name: The name of the member.
        :param int group_id: The ID of the group.
        :return: Nothing
        """
        pass
        
        
    @abc.abstractmethod
    def insert_expense(self, expense, group_id):
        """
        Adds a member to an existing group.
     
        :param expense: The expense to add.
        :type expense: :class:`Expense <xpensemate.data_types.Expense>`
        :param int group_id: The ID of the group.
        :return: Nothing
        """
        pass
        
        
    @abc.abstractmethod
    def insert_transfer(self, transfer, group_id):
        """
        Adds a member to an existing group.
     
        :param transfer: The transfer to add.
        :type transfer: :class:`Transfer <xpensemate.data_types.Transfer>`
        :param int group_id: The ID of the group.
        :return: Nothing
        """
        pass
        
        
    @abc.abstractmethod
    def delete_expense(self, expense_id):
        """
        Deletes an expense
     
        :param int expense_id: The ID of the expense.
        :return: Nothing
        """
        pass
        
        
    @abc.abstractmethod
    def delete_transfer(self, transfer_id):
        """
        Deletes an expense
     
        :param int transfer_id: The ID of the transfer.
        :return: Nothing
        """
        pass

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
        :type member: :class:`xpensemate.data_types.MemberWithCredentials`
        :return: Nothing
        """
        pass
        
        
    @abc.abstractmethod
    def insert_group(self, group):
        """
        Inserts a new member.
     
        :param group: The group to insert.
        :type group: :class:`xpensemate.data_types.Group`
        :return: Nothing
        
        .. Note:: The following happens with the attribute of the argument:
            
            * the :data:`xpensemate.data_types.Group.group_id` field
              of the argument is ignored.
                
            * The keys in its :data:`xpensemate.data_types.Group.member_balances`
              are used to determine the group members. The balance values are ignored.
            
        """
        pass

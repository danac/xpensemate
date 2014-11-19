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

"""
This modules implements some simple containers to store results from the database.

.. Note:: The convention here is that constructors takes **keyword-arguments whose names
    match the attribute names**.
"""

from xpensemate.utils.debt_settling import calculate_debts

class Member:
    def __init__(self, name):
        #: Member name
        self.name = name 


class MemberWithCredentials(Member):
    def __init__(self, password, active, **kwargs):
        super().__init__(**kwargs)
        #: Member password information
        self.password = password
        #: Flag indicating whether the user account is active
        self.active = active


class Group:
    def __init__(self, group_id, name, smallest_unit, owner, member_balance):
        #: Group ID
        self.group_id = group_id
        #: Group name
        self.name = name
        #: Smallest allowed unit for expense and transfer amounts
        self.smallest_unit = smallest_unit
        #: Name of the group owner
        self.owner = owner
        #: Dictionary of (member name, balance) pairs
        self.member_balance = member_balance
        
    @property
    def debts(self):
        """
        Calculate the debts, based on the member balances
        
        :return: A dictionary of dictionary 
            (see :func:`xpensemate.utils.all_partitions.calculate_debts`)
        
        """
        return calculate_debts(self.member_balance)
        

class Expense:
    def __init__(self, expense_id, description, date, amount, maker, members):
        #: Expense ID
        self.expense_id = expense_id
        #: Expense description
        self.description = description
        #: Expense date
        self.date = date
        #: Expense amount
        self.amount = amount
        #: Name of the expense maker
        self.maker = maker
        #: List of member names concerned by this expense
        self.members = members


class Transfer:
    def __init__(self, transfer_id, date, amount, from_member, to_member):
        #: Transfer ID
        self.transfer_id = transfer_id
        #: Transfer date
        self.date = date
        #: Transfer amount
        self.amount = amount
        #: Name of the transfer maker
        self.from_member = from_member
        #: Name of the transfer recipient
        self.to_member = to_member


class GroupWithExpenses(Group):
    def __init__(self, expenses, transfers, **kwargs):
        super().__init__(**kwargs)
        #: List of :class:`Transfer` instances
        self.transfers = transfers
        #: List of :class:`Expense` instances
        self.expenses = expenses

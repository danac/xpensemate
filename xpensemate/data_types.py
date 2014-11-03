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

class Member:
    def __init__(self, member_id, name):
        #: Member ID
        self.id = member_id
        #: Member name
        self.name = name 


class MemberWithCredentials(Member):
    def __init__(self, password_hash, password_salt, hash_function, **kwargs):
        super().__init__(**kwargs)
        #: Hashed member password
        self.password_hash = password_hash
        #: Salt used for the password hash
        self.password_salt = password_salt
        #: Function handle to the hasher
        self.hash_function = hash_function


class Group:
    def __init__(self, group_id, name, member_balances):
        #: Group ID
        self.id = member_id
        #: Group name
        self.name = name
         #: Dictionary of (name, balance) pairs
        self.balances = member_balances
        
        @property
        def members(self):
            """
             List of member names
            """
            return self.balances.keys()
        

class Expense:
    def __init__(self, expense_id, description, date, amount, maker, members):
        #: Expense ID
        self.id = expense_id
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
        #: Expense ID
        self.id = expense_id
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

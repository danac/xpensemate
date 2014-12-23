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
This module contains the form defitions.
"""

import wtforms as wtf
from wtforms.csrf.session import SessionCSRF
import os
import flask

from xpensemate.web import validation


class FormBase(wtf.Form):
    """
    This common form base class contains Cross-Site-Request-Forgery code
    """
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = os.urandom(16)

        @property
        def csrf_context(self):
            return flask.session


class LoginForm(FormBase):
    """
    This class implements the login form.
    """
    
    form_name = "login"
    
    username = wtf.TextField('Username', [
        wtf.validators.DataRequired(),
        validation.wtforms_validation()
    ])
    
    password = wtf.PasswordField('Password', [
        wtf.validators.InputRequired()
    ])
    
    
class ExpenseFormBase(FormBase):
    """
    This base class contains the static part of the expense form.
    Checkboxes for the group members must be dynamically added
    upon instantiation.
    """
    
    form_name = wtf.HiddenField('form_name', [
        wtf.validators.DataRequired()
    ], default="expense")
    
    action = wtf.HiddenField('action', [
        wtf.validators.DataRequired()
    ], default="new")

    date = wtf.DateField('Expense date', [
        wtf.validators.DataRequired()
    ])
    
    description = wtf.TextField('Expense description', [
        wtf.validators.DataRequired()
    ])
    
    amount = wtf.DecimalField('Expense amount', [
        wtf.validators.DataRequired()
    ])
    
    expense_id = wtf.HiddenField('expense_id', [
        wtf.validators.Optional()
    ])
    
            
def expense_form_factory(members):    
    """
    Factory function that dynamically defines and returns a sub-classes
    of :class:`ExpenseFormBase` with one checkbox field per member.
    
    :param list members: A list of member names.
    """
    
    class ExpenseForm(ExpenseFormBase):
        
        def get_member_fields(self):
            return [getattr(self, member) for member in members]
            
        def remove_insertion_fields(self):
            del self.date
            del self.description
            del self.amount
            for member in members:
                delattr(self, member)

    for member in members:
        field = wtf.BooleanField("Expense member ({})".format(member), [
        ])
        setattr(ExpenseForm, member, field)  
    
    return ExpenseForm

    
class TransferFormBase(FormBase):
    """
    This base class contains the static part of the transfer form.
    Checkboxes for the group members must be dynamically added
    upon instantiation.
    """
    
    form_name = wtf.HiddenField('form_name', [
        wtf.validators.DataRequired()
    ], default="transfer")
    
    action = wtf.HiddenField('action', [
        wtf.validators.DataRequired()
    ], default="new")

    date = wtf.DateField('Transfer date', [
        wtf.validators.DataRequired()
    ])
    
    transfer_id = wtf.HiddenField('transfer_id', [
        wtf.validators.Optional()
    ])
            
            
def transfer_form_factory(members):    
    """
    Factory function that dynamically defines and returns a sub-classes
    of :class:`TransferFormBase` with an amount field having a validator
    matching the group's smallest monetary unit.
    """
    
    class TransferForm(TransferFormBase):
            
        def remove_insertion_fields(self):
            del self.date
            del self.amount
            del self.to_member

    amount_field = wtf.DecimalField('Transfer amount', [
        wtf.validators.DataRequired()
    ])

    to_member_field = wtf.RadioField('Transfer receiver', [
        wtf.validators.AnyOf(members)
    ], choices=list(zip(members,members)), default=members[0])
    setattr(TransferForm, 'amount', amount_field)  
    setattr(TransferForm, 'to_member', to_member_field)  
    
    return TransferForm
    
    
    
class GroupForm(FormBase):
    """
    Form used to create and delete groups.
    """
    
    action = wtf.HiddenField('action', [
        wtf.validators.DataRequired()
    ], default="new") 
           
    group_name = wtf.TextField('Group name', [
        wtf.validators.DataRequired()
    ])
    
    group_id = wtf.HiddenField('group_id', [
        wtf.validators.Optional()
    ])
        
    smallest_unit = wtf.DecimalField('Smallest amount', [
        wtf.validators.DataRequired()
    ])

    def remove_insertion_fields(self):
        del self.group_name
        del self.smallest_unit


class NewMemberForm(FormBase):
    """
    Form used to add members to and existing group.
    """
    
    action = wtf.HiddenField('action', [
        wtf.validators.DataRequired()
    ], default="new_member") 
        
    member_name = wtf.TextField('New member name', [
        wtf.validators.DataRequired()
    ])
    
    group_id = wtf.HiddenField('group_id', [
        wtf.validators.Required()
    ])

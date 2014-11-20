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
    
    username = wtf.TextField('Username', [
        wtf.validators.DataRequired(),
        validation.wtforms_validation()
    ])
    
    password = wtf.PasswordField('Password', [
        wtf.validators.InputRequired()
    ])
    
    
class ExpenseFormBase(FormBase):
    """
    This base class contains the static part of a new expense form.
    Checkboxes for the group members must be dynamically added
    upon instantiation.
    """
    
    action = wtf.HiddenField('action', [
        wtf.validators.DataRequired()
    ], default="new")
    
    group_id = wtf.HiddenField('group_id', [
        wtf.validators.DataRequired()
    ])

    date_info = wtf.DateField('Date', [
        wtf.validators.DataRequired()
    ])
    
    description = wtf.TextField('Description', [
        wtf.validators.DataRequired()
    ])
    
    amount = wtf.DecimalField('Amount', [
        wtf.validators.DataRequired(),
        wtf.validators.NumberRange(min=0.0)
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
            del self.date_info
            del self.description
            del self.amount
            for member in members:
                delattr(self, member)

    for member in members:
        field = wtf.BooleanField(member)
        setattr(ExpenseForm, member, field)  
    
    return ExpenseForm



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
This module contains the code used to validate form submissions.
"""

import flask
import wtforms

from xpensemate.config import DBConfig
from xpensemate.utils.numeric import round_to_closest_multiple
from xpensemate import exceptions

class AmountValidator:

    message = "Amount field must be greater than zero and be rounded to the \
        smallest monetary unit."
    
    @staticmethod
    def validate(value, smallest_unit):
        """
        Amount validation function. Forbids null and negative amount and checks
        rounding to the group's smallest monetary unit.
        
        :param str value: the field value
        :param float smallest_unit: the smallest monetary unit
        :rtype: bool
        """
        if float(value) <= 0 or round_to_closest_multiple(value, smallest_unit) != float(value):
            return False
        else:
            return True


class UsernameValidator:

    message = "Username field must not contain space or the '{}' character" \
        .format(DBConfig.string_concat_delimiter)
    
    @staticmethod
    def validate(value):
        """
        Username validation function. Forbids spaces and
        :data:`xpensemate.config.DBConfig.string_concat_delimiter`.
        
        :param str value: the field value
        :rtype: bool
        """
        
        if ' ' in value or DBConfig.string_concat_delimiter in value:
            return False
        else:
            return True


def wtforms_validation(*args, **kwargs):  
    """
    Adapter function that returns a validation function compatible with
    the WTForms validator API that links to the validation method of the
    ``<field.label.text>Validator`` class.
    
    :return: A function handle that takes a ``wtforms.Form`` and a
        ``wtforms.Field`` as arguments and raises ``wtforms.ValidationError``
        if validation fails.
    """
    
    def _validator(form, field):
        FieldValidator = globals()[field.label.text+"Validator"]
        if not FieldValidator.validate(field.data, *args, **kwargs):
            raise wtforms.ValidationError(FieldValidator.message)
            
    return _validator


def flash_form_errors(form):
    """
    Send form validation errors to the client in Flask flash messages.
    
    :param form: A ``wtforms.Form`` instance.
    """
    
    for field, errors in form.errors.items():
        for error in errors:
            flask.flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


def db_access_wrapper(function, *args, **kwargs):
    try:  
        function(*args, **kwargs)
    except exceptions.DatabaseError as e:
        flask.flash("Database error! The data entered is invalid." + str(e), 'error')
        
    except Exception as e:
        flask.flash("An unknown error occurred! Please help us fix this problem by reporting this bug." + "\n" + str(e), 'error')

    
def process_new_delete_form(form, callback_new, callback_delete, args_new = None, args_delete=None):
    member_name = flask.session['username']
    
    redirect = False
    # Do not redirect if there are errors in the forms when inserting
    # because the values entered by the user do not re-appear in the fields
    if flask.request.form['action'] == "new":
        if form.validate():
            
            if args_new is not None:
                db_access_wrapper(callback_new, args_new)
            else:
                db_access_wrapper(callback_new)
            redirect = True
            
        elif form.csrf_token.errors:
            pass
            
        else:
            flash_form_errors(form)
            
    elif flask.request.form['action'] == "delete":
        redirect = True
        
        form.remove_insertion_fields()
        
        if form.validate():
            
            if args_delete is not None:
                db_access_wrapper(callback_delete, args_delete)
            else:
                db_access_wrapper(callback_delete)
            
    else:
        raise ValueError("Bad form action")
    
    return redirect

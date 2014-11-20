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


class UsernameValidator:
    """
    Username validator. Forbids spaces and
    :data:`xpensemate.config.DBConfig.string_concat_delimiter`.
    
    :rtype: bool
    """

    message = "Username field must not contain space or the '{}' character" \
        .format(DBConfig.string_concat_delimiter)
    
    @staticmethod
    def validate(value):
        if ' ' in value or DBConfig.string_concat_delimiter in value:
            return False
        else:
            return True


def wtforms_validation():  
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
        if not FieldValidator.validate(field.data):
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

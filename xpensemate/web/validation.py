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

import random
import string
import flask


CSRF_TOKEN_NAME = "csrf_token"
CSRF_TOKEN_LENGTH = 10


def generate_random_string(length):
    """
    Generate a random string of alphanumeric characters (upper and lower case)
    
    :param int length: Length of the string to generate
    :rtype: str
    """
    alphabet = string.ascii_letters + string.digits
    random_list = [random.choice(alphabet) for i in range(length)]
    return ''.join(random_list)
    
    
def get_csrf_token():
    """
    Stores a random token in the session cookie (if not already present)
    and returns it. Used to prevent Cross-Site-Request-Forgery.
    
    :rtype: str
    """
    
    if CSRF_TOKEN_NAME not in flask.session:
        flask.session[CSRF_TOKEN_NAME] = generate_random_string(CSRF_TOKEN_LENGTH)
    return flask.session[CSRF_TOKEN_NAME]
    
    
def check_csrf_token():
    """
    Check that the CSRF token sent in the POST'd data matches the one in the 
    session cookie.
    """
    if flask.request.method == "POST":
        token = flask.session.pop(CSRF_TOKEN_NAME, None)
        if not token or token != flask.request.form.get(CSRF_TOKEN_NAME):
            flask.abort(403)        

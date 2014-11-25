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

import flask

from xpensemate.web import forms
from xpensemate.db.interface.factory import DatabaseInterfaceFactory


# Get an instance of the backend interface
db_interface = DatabaseInterfaceFactory.get_interface()

#: Flask application blueprint implementing login/logout routes
blueprint = flask.Blueprint('login_blueprint', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login page. Redirects to the root URL upon successful login.
    
    Served on the following routes:
        * /login
        * /login/
    """
    
    form = forms.LoginForm(flask.request.form)
    
    if 'username' in flask.session:
        return flask.redirect('/')
        
    if flask.request.method == 'POST':
        if form.validate():
            username = flask.request.form['username']
            try:
                user = db_interface.get_member_credentials(username)
                flask.session['username'] = username

            except AssertionError:
                flask.flash("Bad credential", 'error')
                
        elif form.csrf_token.errors:
            pass
            
        else:
            validation._errors(form)
            
        return flask.redirect('/login')
        
    return flask.render_template("login.htm", form=form)


@blueprint.route('/logout')
def logout():
    """
    Logout route. Redirects to the root URL.
    
    Served on the following routes:
        * /logout
        * /logout/
    """
    
    # Remove the username from the session if it's there
    flask.session.pop('username', None)
    
    return flask.redirect('/')

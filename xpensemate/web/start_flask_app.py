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

import os
import flask

from xpensemate.db.interface.factory import DatabaseInterfaceFactory
from xpensemate.utils.numeric import round_to_closest_multiple
from xpensemate.web.validation import flash_form_errors
from xpensemate.web.forms import new_expense_form_factory, LoginForm

# We'll need the root path of the web app
ROOT_PATH = os.path.dirname(__file__)

# Get an instance of the backend interface
db_interface = DatabaseInterfaceFactory.get_interface()    

# Instantiate a Flask app
app = flask.Flask(__name__)

# Set the application secret key, used to sign session data
app.secret_key = os.urandom(16)#'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# Insert helper functions into Jinja's namespace
for method in ['round_to_closest_multiple']:
    app.jinja_env.globals[method] = globals()[method]


@app.route("/")
@app.route("/groups")
@app.route("/groups/")
def groups():
    """
    Page displaying the user's groups.
    
    Served on the following routes:
    * /groups
    * /groups/
    """
    
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    member_name = flask.session['username']
    groups = db_interface.get_member_groups(member_name)
    return flask.render_template("groups.htm", groups=groups, member_name=member_name)
    
    
@app.route("/groups/<group_id>", methods=['GET', 'POST'])
def group(group_id):
    """
    Page displaying a detailed view of a group.
    :param int group_id: The ID of the group
    
    Served on the following routes:
        * /groups/<group_id>
    """
    
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
        
    member_name = flask.session['username']
    group = db_interface.get_group_with_movements(group_id)
    groups = db_interface.get_member_groups(member_name)
    
    NewExpenseForm = new_expense_form_factory(group.member_balance.keys())
    form = NewExpenseForm(flask.request.form)

    if flask.request.method == 'POST':
        if form.validate():
            flask.flash("New expense added.", "info")
            return flask.redirect("/groups/" + group_id)
            
        elif form.csrf_token.errors:
            return flask.redirect('/groups/' + group_id)
            
        else:
            flash_form_errors(form)
    
    return flask.render_template("group_expense.htm", group=group, groups=groups, form=form, member_name=member_name)


@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Route to static files, used for development.
    :param str filename: The path to the requested static file.
    
    Served on the following routes:
        * /static/<path:filename>
    """
    return app.send_from_directory(os.path.join(ROOT_PATH, 'static'), filename)    


@app.route('/new_expense', methods=['POST'])
def new_expense():
    flask.flash("Request received!")
    return flask.redirect('/groups/'+flask.request.form.get('group_id'))#str(flask.request.form)
    

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login page. Redirects to the root URL upon successful login.
    
    Served on the following routes:
        * /login
        * /login/
    """
    
    form = LoginForm(flask.request.form)
    
    if 'username' in flask.session:
        return flask.redirect('/')
        
    elif flask.request.method == 'POST':
        if form.validate():
            username = flask.request.form['username']
            try:
                user = db_interface.get_member_credentials(username)
                flask.session['username'] = username
                return flask.redirect('/')
            except AssertionError:
                flask.flash("Bad credential", 'error')
                
        elif form.csrf_token.errors:
            return flask.redirect('/login')
            
        else:
            flash_form_errors(form)
        
    return flask.render_template("login.htm", form=form)


@app.route('/logout')
def logout():
    """
    Logout route. Redirects to the root URL.
    
    Served on the following routes:
        * /logout
        * /logout/
    """
    # remove the username from the session if it's there
    flask.session.pop('username', None)
    return flask.redirect('/')


if __name__ == "__main__":
    
    app.run(debug=True, port=8080)

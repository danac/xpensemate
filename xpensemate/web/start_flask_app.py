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

import os.path
import flask
from xpensemate.db.interface.factory import DatabaseInterfaceFactory

app = flask.Flask(__name__)

ROOT_PATH = os.path.dirname(__file__)

db_interface = DatabaseInterfaceFactory.get_interface()    

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
@app.route("/groups")
@app.route("/groups/")
def groups():
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    member_name = flask.session['username']
    groups = db_interface.get_member_groups(member_name)
    return flask.render_template("groups.htm", groups=groups, member_name=member_name)
    
@app.route("/groups/<group_id>")
def group(group_id):
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    group = db_interface.get_group_with_movements(group_id)
    return flask.render_template("group_expense.htm", group=group)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_from_directory(os.path.join(ROOT_PATH, 'static'), filename)    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        flask.session['username'] = flask.request.form['username']
        return flask.redirect('/')
    return flask.render_template("login.htm")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    flask.session.pop('username', None)
    return flask.redirect(flask.url_for('groups'))


app.run(debug=True, port=8080)

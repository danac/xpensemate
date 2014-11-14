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
from xpensemate.utils.benchmark import timeit

app = flask.Flask(__name__)

ROOT_PATH = os.path.dirname(__file__)
#bottle.TEMPLATE_PATH.insert(0, os.path.join(ROOT_PATH, 'views'))

db_interface = DatabaseInterfaceFactory.get_interface()    

@app.route("/")
@app.route("/groups")
@app.route("/groups/")
def groups():
    member_name = "Dana"
    groups = db_interface.get_member_groups(member_name)
    return flask.render_template("groups.htm", groups=groups, member_name=member_name)
    
@app.route("/groups/<group_id>")
def group(group_id):
    group = db_interface.get_group_with_movements(group_id)
    return flask.render_template("group_expense.htm", group=group)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_from_directory(os.path.join(ROOT_PATH, 'static'), filename)    

#@bottle.get("/static/<filepath:path>")
#def server_static(filepath):
    #return bottle.static_file(filepath, root=os.path.join(ROOT_PATH, 'static'))

app.run(debug=True, port=8080)

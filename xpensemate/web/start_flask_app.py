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
from xpensemate.utils.numeric import format_amount, round_to_closest_multiple
from xpensemate.web.login import blueprint as login_blueprint
from xpensemate.web.groups import blueprint as groups_blueprint
from xpensemate.web.group import blueprint as group_blueprint


# We'll need the root path of the web app
ROOT_PATH = os.path.dirname(__file__)

#: Flask app serving the website
app = flask.Flask(__name__)

# Set the application secret key, used to sign session data
app.secret_key = os.urandom(16)

# Register blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(groups_blueprint)
app.register_blueprint(group_blueprint)

# Get an instance of the backend interface
db_interface = DatabaseInterfaceFactory.get_interface()    

# Insert helper functions into Jinja's namespace
for method in ['round_to_closest_multiple', 'format_amount']:
    app.jinja_env.globals[method] = globals()[method]
    

@app.route('/')
def root():
    return flask.redirect('/groups')
        
@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Route to static files, used for development.
    :param str filename: The path to the requested static file.
    
    Served on the following routes:
        * /static/<path:filename>
    """
    return app.send_from_directory(os.path.join(ROOT_PATH, 'static'), filename)    


if __name__ == "__main__":
    
    # Start the server
    app.run(debug=True, port=8080)

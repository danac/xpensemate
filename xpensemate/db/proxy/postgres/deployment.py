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

from xpensemate.config import DBConfig

import os.path
import psycopg2

SQL_FOLDER = os.path.join(os.path.dirname(__file__), 'sql')
DB_STRUCTURE_FILE = os.path.join(SQL_FOLDER, 'db_structure.sql')
DB_TRIGGERS_FILE = os.path.join(SQL_FOLDER, 'db_triggers.sql')
DB_FUNCTIONS_FILE = os.path.join(SQL_FOLDER, 'db_functions.sql')
DB_PERMS_FILE = os.path.join(SQL_FOLDER, 'db_perms.sql')

def reset_database():
    db_name = DBConfig.database
    db_user = DBConfig.super_user
    db_pass = DBConfig.super_password    
    connection = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    
    with open(DB_STRUCTURE_FILE, 'r') as f:
        structure_sql = f.read()
    with open(DB_TRIGGERS_FILE, 'r') as f:
        triggers_sql = f.read()
    with open(DB_FUNCTIONS_FILE, 'r') as f:
        functions_sql = f.read()
    with open(DB_PERMS_FILE, 'r') as f:
        perms_sql = f.read()
        
    cur = connection.cursor()
    cur.execute(structure_sql)
    cur.execute(triggers_sql)
    cur.execute(functions_sql)
    cur.execute(perms_sql)
    connection.commit()
    cur.close()
    

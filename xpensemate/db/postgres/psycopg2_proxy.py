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

import psycopg2
from xpensemate.db.proxy import AbstractDatabaseProxy

# Convert psycopg2's default Decimal type to regular Python floats
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)


class SingleConnectionProxy(AbstractDatabaseProxy):
    """
    Proxy to the PostgreSQL database engine, using the psycopg2 library
    serving a single connection.
    
    Everytime a query is sent, the following happnes:
    
        #. a cursor is created
        #. the query is executed through that cursor
        #. all the reults are fetched
        #. the connection is committed
        #. the cursor is closed
    
    .. warning:: This class is not green thread-safe!
    """
    
    def __init__(self, database, user, password):
        self.connection = psycopg2.connect(database=database, user=user, password=password)
    
    def query(self, query_string):
        cur = self.connection.cursor()
        try:
            cur.execute(query_string)
            results = cur.fetchall()
        finally:
            self.connection.commit()
            cur.close()
        return results

ProxyClass = SingleConnectionProxy

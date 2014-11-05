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

import hashlib
import base64

class DBConfig:
    """
    This class holds the various database configuration parameters that
    are looked-up at run-time.
    
    .. Note:: Currently, only the UTF-8 encoding is supported.
        The database is assumed to use that encoding.
    """
    
    #: The database backend engine to use, among the ones in
    #: :data:`xpensemate.db.proxy.factory.DatabaseProxyFactory.proxy_module_dispatch`
    engine = "postgres"
    
    #: The database name
    database = "expense"
    
    #: A database user allowed to use the interface selected in :data:`interface`
    user = "xpensemate_function_invoker"
    
    #: The users's password
    password = "lambda"

    #: A database user with admin rights over the database
    super_user = "xpensemate_admin"
    
    #: The super-user's password
    super_password = "lambda"
    
    #: The interface implemented in the database, among the ones in
    #: :data:`xpensemate.db.interface.factory.DatabaseInterfaceFactory.interface_class_dispatch`
    interface = "stored_functions"
    
    #: The character used as delimiter in concatenated strings returned from the database
    string_concat_delimiter = '|'
    
    #: The hashing algorithm used for the user's passwords
    password_hashing_function = lambda x: hashlib.sha512(x.encode("utf-8")).hexdigest()
    
    
    

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

import importlib
from xpensemate.config import DBConfig


class DatabaseProxyFactory:
    """
    Factory class used to automatically instantiate a singleton proxy
    to the database backend defined in
    :class:`xpensemate.config.DBConfig.engine`.
    """
    
    #: Singleton instance of the database proxy
    db_proxy_instance = None
    
    #: Dictionary mapping the possible proxies in
    #: :data:`xpensemate.config.DBConfig.engine` to module paths
    proxy_module_dispatch = {
        "postgres" : "xpensemate.db.proxy.postgres.psycopg2_proxy"
    }
    
    @classmethod
    def get_proxy(cls):
        """
        Returns the unique database proxy, after instantiating it
        if necessary
        
        :return: A singleton instance implementing
                 :class:`AbstractDatabaseProxy <xpensemate.db.proxy.abstract_proxy.AbstractDatabaseProxy>`
         """
        
        if cls.db_proxy_instance is None:
            cls._instantiate_proxy_instance()
        
        return cls.db_proxy_instance
        
        
    @classmethod
    def _instantiate_proxy_instance(cls):
        try:
            engine = DBConfig.engine
            module_path = cls.proxy_module_dispatch[engine]
            module = importlib.import_module(module_path) 
            
            db_name = DBConfig.database
            db_user = DBConfig.user
            db_pass = DBConfig.password
            cls.db_proxy_instance = module.ProxyClass(db_name, db_user, db_pass)
            
        except KeyError:
            message = "Database backend not implemented: {}".format(engine)
            raise NotImplementedError(message)

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

import abc


class AbstractDatabaseProxy(metaclass=abc.ABCMeta):
    """
    This class describes the interface of a proxy to a datdabase engine.
    """
    
    @abc.abstractmethod
    def query(query_string): # pragma: no cover
        """
        Method used to execute queries on the database.
        
        :param str query_string: The query string
        :return: An iterable over the result set
        """
        pass
 

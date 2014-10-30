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

from ..utils import optimal_solve

class BackendInterface:
    """
    This class contains the interface to the storage and expense management
    backend that is expected by the rest of the code.
    
    """
    
    def get_member(user_name):
        """
        Must return a whole user record
     
        Parameters
        ----------
        user_name : string
            The name of the user.
     
        Returns
        -------
        user_t : list
            Returns the user information.
        
        Raises
        ------
            NotImplemented
        """
        pass
    

class InterfaceToStoredProcedures(BackendInterface):
    """
    This class implements the backend interface from :class:`.BackendInterface`
    by using a set of stored procedures expected to be implemented in a backend database.

    It relies on a database connection object implementing a `query` method that
    returns an iterable.

    """
    pass
    

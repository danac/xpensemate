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
  
import time

def timeit(f):
    """
    Decorator printing the running time of the wrapped function.
    
    Usage:
    
    .. code-block:: python
        
        @timeit
        def function(arguments):
            pass
        
    """
    def timer(*args, **kwargs):
        t=time.time()
        result = f(*args, **kwargs)
        t2=time.time()
        print("[{}]Running time: {:e} sec".format(f.__name__, t2 - t))
        return result
    return timer

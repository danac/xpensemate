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

import collections
import functools
import copy

def lru_cache(maxsize=100):
    '''
    Re-implementation of the "Least Recently Used" from ``functools.lru_cache``
    that "deep-copies" the return values of the wrapped function.
    This is necessary for the proper handling of compound return values that
    can get partially deallocated.

    Arguments to the wrapped function must all be hashable.
    
    The type-based partial caching of arguments found in ``functools.lru_cache``
    is not implemented (no ``Typed`` option).
    
    Usage:
        
    .. code-block:: python
        
        @lru_cache(maxsize=50)
        def function(arguments):
            pass

    '''
    def decorating_function(function):
        cache = collections.OrderedDict()
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            key = repr(args)
            if kwargs:
                key += repr(tuple(sorted(kwargs.items())))
            try:
                result = cache.pop(key)
                #print("Cache hit")
            except KeyError:
                #print("Cache miss")
                result = function(*args, **kwargs)
                if len(cache) >= maxsize:
                    cache.popitem(0)
            cache[key] = copy.deepcopy(result)
            return result
        return wrapper
    return decorating_function

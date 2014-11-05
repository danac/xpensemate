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


from xpensemate.utils._partition_list_inline import partitions as p

class PartitionList:
    """
    Wrapper around a dictionary of all partitions of a set into
    subsets of size larger than 1.
    
    Exposes a dictionary interface, with the following contents:

    .. code-block:: python
    
        {
         0: [],
         1: [],
         2: [],
         3: [],
         4: [[[1, 2], [0, 3]], [[1, 3], [0, 2]], [[0, 1], [2, 3]]],
         5: [[[1, 2, 3], [0, 4]],
          [[0, 1, 4], [2, 3]],
          [[1, 4], [0, 2, 3]],
          [[1, 2, 4], [0, 3]],
          [[0, 1, 3], [2, 4]],
          [[1, 3], [0, 2, 4]],
          [[0, 1, 2], [3, 4]],
          [[1, 2], [0, 3, 4]],
          [[1, 3, 4], [0, 2]],
          [[0, 1], [2, 3, 4]]],
         ...
        }
        
    """    
    def __init__(self):
        self.partitions = p
    
    def __getitem__(self, key):
        return self.partitions[key]
        
    def __setitem__(self, key, value):
        self.partitions[key] = value
        
    def __repr__(self):
        return "{l:[[[i,j,...], ...], ...], ...}"

#: Instance of :class:`PartitionList`.
partitions = PartitionList()

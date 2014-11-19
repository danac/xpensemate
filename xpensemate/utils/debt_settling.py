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

"""
This module contains the code used to compute debts among members of
a group.
"""

from xpensemate.utils.partitioning import find_zero_balance_subsets
from xpensemate.utils import benchmark


#: Absolute tolerance used to determine if a floating-point numbe ris null.
TOL = 1e-6


def is_null(x):
    """
    Helper function used to assert that a floating-point number is null.
    The tolerance is defined by :data:`TOL`.
    
    :param float x: The number to consider.
    :rtype: bool
    
    """
    return abs(x) < TOL


class MemberBalance:
    """
    Simple container of a name-balance pair implementing comparison, addition
    and hash operations.
    """
    
    def __init__(self, name, balance):
        #: String
        self.name = name
        #: Value which can be compared and added.
        self.value = balance
    
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.value < other.value
        else:
            return self.value < other
    
    def __hash__(self):
        return self.name.__hash__()
        
    def __bool__(self):
        return self.value != 0
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.value + other.value
        else:
            return self.value + other
    
    __radd__ = __add__
        
    def __repr__(self):
        return '"{}":{}'.format(self.name, self.value)
            

def maximum_bipartite_matching(objects):
    """
    Find the maximum bipartite matching between positive and negative values
    in a list which sum up to zero.
    
    :param list objects: A list of objects with a readable ``name`` attribute
        and a writable ``value`` attribute. The same of all values in the list
        must be zero.
        
    :return: A dictionary of dictionaries describing the flow of the matching
        as follows
        
    .. code-block:: python
    
        {
            'Member X':
            {
                'Member Y': 4,
                'Member Z': 6.8,
                ...
            },
            ...
        }    
        

    """
    
    if not any(objects):
        return {}
    b = sorted(objects)
    i = j = 0
    N = len(objects)
    transfers = {}
    
    while i != N and j != N:
        if b[i].value <= 0:
            i += 1
        elif b[j].value >= 0:
            j += 1
        else:
            if b[i].value < -b[j].value:
                m = b[i].value
            else:
                m = -b[j].value
            if not b[i].name in transfers:
                transfers[b[i].name] = {}
                
            transfers[b[i].name][b[j].name] = m
                
            #print("{}->{}:{}".format(i,j,m))
            b[i].value = b[i].value - m
            b[j].value = b[j].value + m
    
    return transfers
    
def merge_dicts(dict1, dict2):
    """
    Merge two dictionaries whose values are dictionaries.
    
    :param dict d1: A dictionary whose values are themselves (possibly empty)
        dictionaries.
    :param dict d2: A dictionary whose values are themselves (possibly empty)
        dictionaries.
    :return: A generator of (key, value) tuples.
    
    .. code-block:: python
    
        d1 = {
            'Key1': {},
            'Key2': {
                'Subkey1': {}
            }
        }
        
        d2 = {
            'Key3': {},
            'Key2': {
                'Subkey3': {}
            }
        }
        
        merge_dicts(d1,d2) = {
            'Key1': {},
            'Key2': {
                'Subkey1': {},
                'Subkey3': {}
            },
            'Key3': {}
        }
        
    """
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            yield (k, dict(mergedicts(dict1[k], dict2[k])))
        elif k in dict1: 
            yield (k, dict1[k])
        else: 
            yield (k, dict2[k]) 


def calculate_debts(d, enable_partitioning=True):
    """
    Compute the debts based on a set of balances.
    
    :param dict d: Dictionary of balances indexed by member name.
    :param bool enable_partitioning: Enable the search for subset of members
        that can settle their debts on their own (can take time for large groups).
        Even if this parameter is set to True, partitioning is performed only if
        the partition list is implemented for the right size in
        :data:`xpensemate.utils.partition_list.partitions`.
    
    :return: A dictionary of dictionaries, identical to the output of
        :func:`maximum_bipartite_matching`.
        
    """
    typed_l = []
    for k in d:
        typed_l.append(MemberBalance(k, d[k]))
    assert is_null(sum(typed_l))
    #print("Set cardinality {}".format(len(typed_l)))
    
    if enable_partitioning:
        parts = find_zero_balance_subsets(typed_l)
    else:
        parts = [typed_is_suml]
    #print("Using a {}-partition".format(len(parts)))
    
    transfers = {}
    for part in parts:
        assert is_null(sum(part)), "Bad partitioning error."
        new_transfers = maximum_bipartite_matching(part)
        transfers = dict(merge_dicts(transfers, new_transfers))
        
    num_transfers = 0
    for key, val in transfers.items():
        num_transfers += len(val)
    #print("Total number of bipartite matches {}".format(num_transfers))
    
    return transfers


if __name__ == "__main__":
    from decimal import Decimal
    #l = (5, 3.3, -5, -4, 9, -9.2, 11, -6.8, -3.3)#, -5, -4, -1)
    #print("Testing with list:", l)
    #assert is_null(sum(l))
    #d = {str(k):k for k in l}
    d={'Dana': Decimal('3.3336666666666667'), 'Andy': Decimal('-0.0003333333333333'), 'Victoria': Decimal('-3.3333333333333333')}
    result = calculate_debts(d, 0.05)
    print(result)

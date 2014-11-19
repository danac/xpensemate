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

from xpensemate.utils.partitioning import apply_partitions
from xpensemate.utils import benchmark

TOL = 1e-6


def is_sum_null(l):
    return abs(sum(l)-0) < TOL


def find_zero_balance_subsets(l):
    """
    Given a list of summable items, this finds subsets of the list whose
    elements sum up to zero. This function calls
    :func:`xpensemate.utils.partitioning.apply_partitions`. It returns the argument
    as is if the partitioning is not implemented for the right size.
    
    :param list l: A list of summable elements.
    :return: A list of list describing the partitioning.
    """
    try:
        for i in apply_partitions(l):
            #print("--Checking {}".format(len(i)))
            flag = True
            for j in i:
                flag = flag and is_sum_null(j)
            if flag:
                return parts
    except NotImplementedError:
        return l,
    return l,


class MemberBalance:
    """
    Simple container of a name-balance pair implementing comparison, addition
    and hash operations.
    """
    
    def __init__(self, name, balance):
        #: String
        self.name = name
        #: Value which can be compared and added.
        self.balance = balance
    
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.balance < other.balance
        else:
            return self.balance < other
    
    def __hash__(self):
        return self.name.__hash__()
        
    def __bool__(self):
            return self.balance != 0
            
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.balance + other.balance
        else:
            return self.balance + other
    
    __radd__ = __add__
        
        
    def __repr__(self):
        return '"{}":{}'.format(self.name, self.balance)
            
    __nonzero__ = __bool__


def bipartite_matching(balances):
    
    if not any(balances):
        return {}
    b = sorted(balances)
    i = j = 0
    N = len(balances)
    transfers = {}
    while i != N and j != N:
        if b[i].balance <= 0:
            i += 1
        elif b[j].balance >= 0:
            j += 1
        else:
            if b[i].balance < -b[j].balance:
                m = b[i].balance
            else:
                m = -b[j].balance
            if not b[i].name in transfers:
                transfers[b[i].name] = {}
                
            transfers[b[i].name][b[j].name] = m
                
            #print("{}->{}:{}".format(i,j,m))
            b[i].balance = b[i].balance - m
            b[j].balance = b[j].balance + m
    
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


def calculate_debts(d, smallest_unit, enable_partitioning=True):
    typed_l = []
    for k in d:
        typed_l.append(MemberBalance(k, d[k]))
    assert is_sum_null(typed_l)
    #print("Set cardinality {}".format(len(typed_l)))
    
    if enable_partitioning:
        parts = find_zero_balance_subsets(typed_l)
    else:
        parts = [typed_is_suml]
    #print("Using a {}-partition".format(len(parts)))
    
    transfers = {}
    for part in parts:
        assert is_sum_null(part), "Bad partitioning error."
        new_transfers = bipartite_matching(part)
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
    #assert is_sum_null(l)
    #d = {str(k):k for k in l}
    d={'Dana': Decimal('3.3336666666666667'), 'Andy': Decimal('-0.0003333333333333'), 'Victoria': Decimal('-3.3333333333333333')}
    result = calculate_debts(d, 0.05)
    print(result)

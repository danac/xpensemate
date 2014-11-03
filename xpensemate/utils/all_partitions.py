import time
import functools

from xpensemate.utils.partitioning import apply_partitions
from xpensemate.utils import benchmark

TOL = 1e-10


#@benchmark.timeit
def partition_balances(l):
    #print(len(list(neclusters3(l,3))))
    """
    This finds partitions of a given list of balances where the total balance
    of each element of the partition is null (NP-complete)
    """
    try:
        for i in apply_partitions(l):
            #print("--Checking {}".format(len(i)))
            flag = True
            for j in i:
                flag = flag and (abs(sum(j)-0) < TOL)
            if flag:
                parts = map(tuple, i)
                return tuple(parts)
    except NotImplementedError:
        return l,


class MemberBalance:
    
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
    
    #def __cmp__(self, other):
        #if self.balance < other.balance:
            #return -1
        #elif self.balance > other.balance:
            #return 1
        #else:
            #return 0
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


#@timing
#@lru_cache()
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
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            yield (k, dict(mergedicts(dict1[k], dict2[k])))
        elif k in dict1: 
            yield (k, dict1[k])
        else: 
            yield (k, dict2[k]) 
  

def is_sum_null(l):
    return (sum(l)-0) < TOL
  

#@benchmark.timeit
def calculate_debts(l, enable_partitioning=True):
    typed_l = []
    for i in l:
        typed_l.append(MemberBalance(str(i), i))
    typed_l = tuple(typed_l)
    #print("Set cardinality {}".format(len(typed_l)))
    
    if enable_partitioning:
        parts = partition_balances(typed_l)
    else:
        parts = (typed_l,)
    #print("Using a {}-partition".format(len(parts)))
    
    transfers = {}
    for part in parts:
        assert is_sum_null(part), "Bad partitioning error."
        new_transfers = bipartite_matching(part)
        transfers = dict(merge_dicts(transfers, new_transfers))
        
    #num_transfers = 0
    #for key, val in transfers.items():
        #num_transfers += len(val)
    #print("Total number of bipartite matches {}".format(num_transfers))
    
    return transfers


if __name__ == "__main__":
    l = (5, 3.3, -5, -4, 9, -9.2, 11, -6.8, -3.3)#, -5, -4, -1)
    print("Testing with list:", l)
    assert is_sum_null(l)
    result = calculate_debts(l)
    print(result)

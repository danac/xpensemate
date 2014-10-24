import time
from cache import lru_cache
import functools
import copy

"""
http://stackoverflow.com/questions/18353280/iterator-over-all-partitions-into-k-groups
"""

def clusters(l, K):
    if len(l) > 0:
        prev = None
        for t in clusters(l[1:], K):
            tup = sorted(t)
            if tup != prev:
                prev = tup
                for i in range(K):
                    #print(len(tup[:i]), tup[:i])
                    yield tup[:i] + [[l[0]] + tup[i],] + tup[i+1:]
    else:
        yield [[] for _ in range(K)]
            
def neclusters3(l, K):
    for c in clusters(l, K):
        if all(x for x in c): yield c

def timing(f):
    def timer(*args, **kwargs):
        t=time.time()
        result = f(*args, **kwargs)
        t2=time.time()
        print("Running time: {:e} seconds".format(t2-t))
        return result
    return timer


#@timing
@lru_cache()
def partition(l):
    #print(len(list(neclusters3(l,3))))
    """
    This finds partitions of a given list of balances where the total balance
    of each element of the partition is null (NP-complete)
    """
    for k in range(len(l)-1, 1, -1):
        #print("Evaluating {}-partitions".format(k))
        for i in neclusters3(l,k):
            flag = True
            for j in i:
                flag = flag and (sum(j) == 0)
            if flag:
                parts = map(tuple, i)
                return tuple(parts)
    return l

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
@lru_cache()
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
    
def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            yield (k, dict(mergedicts(dict1[k], dict2[k])))
        elif k in dict1: 
            yield (k, dict1[k])
        else: 
            yield (k, dict2[k]) 
  
@timing
@lru_cache()
def optimal_solve(l, partitioning=True):
    typed_l = []
    for i in l:
        typed_l.append(MemberBalance(str(i), i))
    typed_l = tuple(typed_l)
    print("Set cardinality {}".format(len(typed_l)))
    if partitioning:
        parts = partition(typed_l)
    else:
        parts = (typed_l,)
    print("Found {}-way partition".format(len(parts)))
    transfers = {}
    for part in parts:
        new_transfers = bipartite_matching(part)
        transfers = dict(mergedicts(transfers, new_transfers))
    print("Total number of bipartite matches {}".format(len(transfers)))
    return transfers
    
l = (5, 3, -5, -3, 9, -9, 10, -7, -3)#, -5, -4, -1)

result = optimal_solve(l)
print(result)
print("---")
result = optimal_solve(l, False)
result = optimal_solve(l, False)
print(result)
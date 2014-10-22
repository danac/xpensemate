import time

"""
http://stackoverflow.com/questions/18353280/iterator-over-all-partitions-into-k-groups
"""

def clusters(l, K):
    if l:
        prev = None
        for t in clusters(l[1:], K):
            tup = sorted(t)
            if tup != prev:
                prev = tup
                for i in range(K):
                    yield tup[:i] + [[l[0]] + tup[i],] + tup[i+1:]
    else:
        yield [[] for _ in range(K)]
            
def neclusters3(l, K):
    for c in clusters(l, K):
        if all(x for x in c): yield c
        
l = [5, 3, -5, -3]#, 9, -9]


#print(len(list(neclusters3(l,3))))
t=time.time()
"""
This finds partitions of a given list of balances where the total balance
of each element of the partition is null (NP-complete)
"""
for k in range(2,len(l)):
    for i in neclusters3(l,k):
        flag = True
        for j in i:
            flag = flag and (sum(j) == 0)
            #print(sum(j)),
        #print(flag)
        if flag:
            for j in i:
                print(j),
            print("")
            print("--")

t2=time.time()-t
print(t2)


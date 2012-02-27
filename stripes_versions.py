import json
import hashlib
s=raw_input()
#s=r'["parent: 70d5c5867b4e5f23f2528555539570a06cee7e05\nIIR","parent: e20a83f79618704c87f9922d301b3587e9aed03b\nparent: 3b059cb02ee31cefa2fe32bc2695d70f9c4122fc\noxy","parent: 4142c354781c366af60b52d9e8cab8bc3506b104\nPmS"]'
J=json.loads(s)
D=[]
# First time through identify valid ids
H={} # Set of valid hex digests
for i,j in enumerate(J):
    s=hashlib.sha1(j)
    t=intern(s.hexdigest())
    H[t]=i
# Second time through look at parents and count how many we have to emit first
from collections import defaultdict
D=defaultdict(list) # list of children for each commit hex digest
counts=[0]*len(J) # For each commit, number of parents we need to emit first
E=[] # Commits to make

# Each entry says which it is the parent of.
for i,j in enumerate(J):
    A=j.split('\n')
    c=0
    for p in A[:-1]:
        child=intern(str(p[8:]))
        if child not in H:
            continue
        # Now we need to note which children
        childi=H[child]
        counts[childi]+=1
        D[i].append(childi)
e=0
A=[]
# We can now emit any with zero counts
for i,c in enumerate(counts):
    if c==0:
        E.append(i)
while e<len(E):
    i=E[e]
    A.append(J[i])
    for c in D[i]:
        counts[c]-=1
        if counts[c]==0:
            E.append(c)
    e+=1
assert e==len(J)
print json.dumps(A,separators=(',', ':'))

    
        
        
    

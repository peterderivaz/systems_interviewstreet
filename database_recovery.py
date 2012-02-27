
import sys
from collections import defaultdict

def make_price(s):
    """Given a string $4.56 returns price in cents"""
    assert s[0]=='$'
    s=s[1:]
    if '.' not in s:
        return int(s)*100
    A=s.split('.')
    return int(A[0])*100+int(A[1])

def str_price(x):
    """Invert make_price"""
    #x=int(x+0.5)
    return '$%.2f' % (x/100)
    x=int(x)
    cents=x%100
    dollars=x//100
    return '$%d.%.2d' %(dollars,cents)

def str_price_signed(x):
    """Invert make_price and add sign at front"""
    #x=int(x+0.5)
    if x==0: return 'average'
    if x<0:
        return '-'+str_price(-x)
    return '+'+str_price(x)

C=defaultdict(int)
D=[]
for s in sys.stdin.readlines():
    s=s.rstrip()
    A=s.split()
    name=A[0]
    price=make_price(A[1])
    cities=A[2:]
    for c in cities:
        C[c]+=1
    D.append((name,price,cities))

children=defaultdict(set)
agents=defaultdict(list)
cost=defaultdict(int)
num=defaultdict(int)
# The key is that the count for each node must be smaller as we go up the hierarchy
for name,price,cities in D:
    S=sorted([(C[c],c) for c in cities],reverse=True)
    if len(set(n for n,c in S))!=len(S):
        print 'ambiguous hierarchy'
        break
    # Now construct graph of parents
    last='top_level'
    for i,(count,c) in enumerate(S):
        # Always add price to parents
        cost[c]+=price
        num[c]+=1
        children[last].add(c)
        last=c
    # And place agent into the right zone
    agents[last].append((name,price))
else:
    mean={}
    for c,price in cost.items():
        n=num[c]
        mean[c]=float(price)/n
        # mean[c]=int(0.5+float(price)/n) # gets 1,2,6,7,8 correct
    # If got here we have an unambiguous hierarchy to emit
    def emit(node,x=''):
        """For each child print out name of area, agents, children in sorted order, and using x prefix"""
        for c in sorted(children[node]):
            if len(x)==0:
                print x+c+' '+str_price(mean[c])
            else:
                print x+c+' '+str_price(mean[c])+' ('+str_price_signed(mean[c]-mean[node])+')'
            for name,price in sorted(agents[c]):
                print x+'  - '+name+' '+str_price(price)
            emit(c,x+'  ') 
    emit('top_level')
        


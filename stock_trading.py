def compute_profit(P):
    """Strategy is to precompute best subsequent price.
    Buy if lower, sell all we have if higher"""
    highest=P[-1]
    profit=0
    for p in P[::-1]:
        if p<highest:
            profit+=highest-p
        else:
            highest=p        
    return profit

T=input()
for t in xrange(T):
    N=input()
    P=[]
    while len(P)<N:
      P=P+map(int,raw_input().split())
    print compute_profit(P)

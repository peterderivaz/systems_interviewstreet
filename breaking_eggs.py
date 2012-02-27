N=300
M=300
F=[[0]*(N+1) for m in xrange(M+1)]
G=[[0]*(N+1) for m in xrange(M+1)]
# Critical height c means that egg thrown strictly above c will break

# F[m][n] gives the number of throws to determine the critical height
# with m eggs, given that the critical height is 0<=c<=n

# G[m][n] gives the number of throws given that the critical height is 0<=c<=n
# and we have already thrown one egg at height n and it did not break

# Strategy for G is to use the thrown egg
# Strategy for F is to throw one egg at n
# This will never break so may as well throw at top.
big=1000000
G[0]=[big]*(N+1) # If have no eggs left then can only determine n if it is 0
G[0][0]=0
F[0]=[big]*(N+1)
F[0][0]=0

# This recurrence could be made to go much faster if necessary
# For example, note that G[m] and F[m] will always be increasing sequences
# so the minimum could be found by bisection.
for m in xrange(1,M+1):
    for n in xrange(1,N+1):
        g=min(max(G[m][n-k],F[m-1][(k-1)]) for k in xrange(1,n+1))
        G[m][n]=g+1
        F[m][n]=g+2

T=input()
for t in xrange(T):
    N,M=map(int,raw_input().split()[:2])
    print F[M][N]

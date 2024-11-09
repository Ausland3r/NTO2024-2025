import numpy as np
n, m = [int(x) for x in input().split()]
summer = np.zeros((n, m), dtype=int)
q = int(input())
for i in range(q):
    x, y, h, v = [int(z) for z in input().split()]
    q = np.tri(h, dtype=int)*v
    summer[n-(y+h)+1:n-(y+h)+1+h, x-1:x+h-1] += q

np.savetxt('output.txt', summer, delimiter=' ', fmt='%d')

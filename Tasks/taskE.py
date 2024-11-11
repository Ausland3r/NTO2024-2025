import numpy as np
f = open('input.txt', 'r')
n, m = [int(x) for x in f.readline().split()]
summer = np.zeros((n, m), dtype=int)
q = int(f.readline())
q1 = np.tri(min(n, m), dtype=int)
for i in range(q):
    x, y, h, v = [int(z) for z in f.readline().split()]
    q = np.tri(h, dtype=int)*v
    summer[n-(y+h)+1:n-(y+h)+1+h, x-1:x+h-1] += q1[:h, :h] * v

np.savetxt('output.txt', summer, delimiter=' ', fmt='%d')

# coding: utf-8
# (c) 2016-02-10 Teruhisa Okada

import numpy as np
from numba.decorators import jit

@jit
def zslice(q, p, p0, mask_val=np.NaN):
    N, M, L = q.shape[0], q.shape[1], q.shape[2]

    q_iso = np.empty((M, L))
    for i in range(L):
        for j in range(M):
            q_iso[j, i] = mask_val
            for k in range(N-1):
                if (((p[k, j, i] < p0) and (p[k+1, j, i] > p0)) or
                    ((p[k, j, i] > p0) and (p[k+1, j, i] < p0))):
                    dp = p[k+1, j, i] - p[k, j, i]
                    dp0 = p0 - p[k, j, i]
                    dq = q[k+1, j, i] - q[k, j, i]
                    q_iso[j, i] = q[k, j, i] + dq*dp0/dp
    return q_iso


if __name__ == '__main__':
    p = np.linspace(-100, 0, 30)[:, None, None] * np.ones((50, 70))
    x, y = np.mgrid[0:20:50j, 0:20:70j]
    q = np.sin(x) + p
    p0 = -50.

    print zslice(q, p, p0)
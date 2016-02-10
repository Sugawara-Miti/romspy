# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

import numpy as np
import pandas as pd


def ramp(zeta):
    for i in xrange(744):
        zeta[i] = zeta[i] * i / 744.0 + 150.0 * (1.0 - i / 744.0)
    return zeta


def bry_zeta(dims, zetafile):
    print 'bry_zeta:', zetafile
    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    zeta = {}
    zeta = pd.read_csv(zetafile, index_col='date')
    for name in zeta.columns.values:
        zeta[name] = ramp(zeta[name].values)
    print zeta
    th = len(zeta)
    zeta_out = {}
    zeta_out['w'] = np.ndarray(shape=[th, eta_rho])
    zeta_out['s'] = np.ndarray(shape=[th, xi_rho])
    for eta in xrange(eta_rho):
        tk = zeta.tk.values / 100.0
        ei = zeta.ei.values / 100.0
        if eta < 68:
            zeta_out['w'][:, eta] = ei
        elif eta > 121:
            zeta_out['w'][:, eta] = tk
        else:
            a = eta - 68
            b = 121 - eta
            zeta_out['w'][:, eta] = (a*tk + b*ei) / (a+b)
    for xi in xrange(xi_rho):
        ka = zeta.ka.values / 100.0
        nu = zeta.nu.values / 100.0
        if xi < 2:
            zeta_out['s'][:, xi] = nu
        elif 67 < xi:
            zeta_out['s'][:, xi] = ka
        else:
            a = xi - 2
            b = 67 - xi
            zeta_out['s'][:, xi] = (a*ka + b*nu) / (a+b)
    return zeta_out

if __name__ == '__main__':
    HOME = ''
    dims = {'xi':117, 'eta':124, 's':20}
    zetafile = 'F:/okada/Dropbox/Data/zeta_op_2012.csv'
    zeta = bry_zeta(dims, zetafile)

    def plot():
        import matplotlib.pyplot as plt
        #plt.pcolor(zeta['s'][:200,:])
        plt.plot(zeta['w'][:200,68])
        plt.plot(zeta['w'][:200,120])
        plt.plot(zeta['s'][:200,3])
        plt.plot(zeta['s'][:200,67])
        plt.show()
    plot()

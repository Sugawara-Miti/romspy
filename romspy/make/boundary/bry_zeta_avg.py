# coding: utf-8
# (c) 2015-11-19 Teruhisa Okada

"""
沼島・海南の平均，および高砂・江井の平均値に変更
"""

import numpy as np
import pandas as pd


def ramp(zeta):
    for i in xrange(744):
        zeta[i] = zeta[i] * i / 744.0 + 150.0 * (1.0 - i / 744.0)
    return zeta


def bry_zeta_avg(dims, zetafile):
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

    zeta['west'] = (zeta.tk + zeta.ei) / 2.0
    zeta['south'] = (zeta.ka + zeta.nu) / 2.0
    for eta in xrange(eta_rho):
        zeta_out['w'][:, eta] = zeta.west.values / 100.0
    for xi in xrange(xi_rho):
        zeta_out['s'][:, xi] = zeta.south.values / 100.0
    return zeta_out


def bry_zeta_avg2(dims, zetafile):
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

    zeta['west'] = (zeta.tk + zeta.ei) / 2.0
    zeta['south'] = (zeta.ka + zeta.nu) / 2.0
    for eta in xrange(eta_rho):
        if eta < 20:
            zeta_out['w'][:, eta] = zeta.south.values / 100.0
        else:
            zeta_out['w'][:, eta] = zeta.west.values / 100.0
    for xi in xrange(xi_rho):
        zeta_out['s'][:, xi] = zeta.south.values / 100.0
    return zeta_out

if __name__ == '__main__':
    HOME = ''
    dims = {'xi':117, 'eta':124, 's':20}
    zetafile = 'F:/okada/Dropbox/Data/boundary/zeta_op_2012.csv'
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

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


def bry_zeta_dat(dims, zetafiles):
    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    zeta = {}
    for i in xrange(4):
        print 'bry_zeta_dat:', zetafiles[i],
        zeta[i] = pd.read_csv(zetafiles[i], skiprows=2, names=['date', 'z0', 'tp'])
        print np.mean(zeta[i]['z0']),
        zeta[i]['z0'] = ramp(zeta[i]['z0'][:])
    th = len(zeta[i])
    zeta_out = {}
    zeta_out['w'] = np.ndarray(shape=[th, eta_rho])
    zeta_out['s'] = np.ndarray(shape=[th, xi_rho])
    for eta in xrange(eta_rho):
        takasago = zeta[3]['z0'] / 100.0
        ei = zeta[1]['z0'] / 100.0
        if eta < 68:
            zeta_out['w'][:, eta] = ei
        elif eta > 121:
            zeta_out['w'][:, eta] = takasago
        else:
            a = eta - 68
            b = 121 - eta
            zeta_out['w'][:, eta] = (a*takasago + b*ei) / (a+b)
    for xi in xrange(xi_rho):
        kainan = zeta[2]['z0'] / 100.0
        awazu = zeta[0]['z0'] / 100.0
        if 67 < xi:
            zeta_out['s'][:, xi] = kainan
        else:
            a = xi + 22
            b = 67 - xi
            zeta_out['s'][:, xi] = (a*kainan + b*awazu) / (a+b)
    return zeta_out

if __name__ == '__main__':
    HOME = 'F:/okada/Dropbox/Data/boundary/'
    HOME = '/home/okada/Dropbox/Data/boundary/'
    dims = {'xi':117, 'eta':124, 's':20}
    zeta = [HOME+'zeta_hour/2012_Awazu/zeta.dat',
            HOME+'zeta_hour/2012_Ei/zeta.dat',
            HOME+'zeta_hour/2012_Kainan/zeta.dat',
            HOME+'zeta_hour/2012_Takasago/zeta.dat']
    zeta = bry_zeta_dat(dims, zeta)

    def plot():
        import matplotlib.pyplot as plt
        #plt.pcolor(zeta['s'][:200,:])
        plt.plot(zeta['w'][:200,68])
        plt.plot(zeta['w'][:200,120])
        plt.plot(zeta['s'][:200,3])
        plt.plot(zeta['s'][:200,67])
        plt.show()
    #plot()

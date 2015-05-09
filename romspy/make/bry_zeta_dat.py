# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

# import 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def ramp(zeta):
    for i, z in enumerate(zeta):
        if i <= 300:
            zeta[i] = z * i / 300.0
    return zeta

def bry_zeta_dat(dims, zetafiles):
    
    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    
    zeta = {}
    for i in xrange(4):

        print 'bry_zeta_dat:', zetafiles[i]
    
        zeta[i] = pd.read_csv(zetafiles[i], skiprows=2, names=['date', 'z0', 'tp'] )
        zeta[i]['z0'] = ramp( zeta[i]['z0'][:] )
        #plt.plot( zeta[i]['z0'] )
        #plt.savefig('check_zeta{}.png'.format(i))
    
    th = len(zeta[i])
    
    zeta_out = {}
    zeta_out['w'] = np.ndarray(shape=[th, eta_rho])
    zeta_out['s'] = np.ndarray(shape=[th, xi_rho])
    
    for eta in xrange(eta_rho):
        zeta_out['w'][:, eta] = zeta[0]['z0'] / 100.0 ### Attention!!! ###
    
    for xi in xrange(xi_rho):
        zeta_out['s'][:, xi]  = zeta[1]['z0'] / 100.0 ### Attention!!! ###
        
    return zeta_out

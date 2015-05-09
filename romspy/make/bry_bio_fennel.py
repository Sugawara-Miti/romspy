# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

import numpy as np
import pandas as pd

def bry_bio_fennel(dims, csvfiles):

    print 'bry_bio_fennel:', 'w', csvfiles['w']
    print 'bry_bio_fennel:', 's', csvfiles['s']

    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    s_rho   = dims['s']

    bio_w = pd.read_csv(csvfiles['w'], skiprows=[1], parse_dates='time', index_col='time')
    bio_s = pd.read_csv(csvfiles['s'], skiprows=[1], parse_dates='time', index_col='time')

    bio_names = bio_w.columns
    N = ['NO3', 'NH4', 'LDeN', 'SDeN']
    P = ['PO4', 'LDeP', 'SDeP']
    O = ['oxygen', 'COD', 'H2S']

    for name in bio_names:
        if name in N:
            bio_w[name] = bio_w[name].apply( lambda v: v/14.0*1000.0 )
            bio_s[name] = bio_s[name].apply( lambda v: v/14.0*1000.0 )
            
        elif name in P:
            bio_w[name] = bio_w[name].apply( lambda v: v/31.0*1000.0 )
            bio_s[name] = bio_s[name].apply( lambda v: v/31.0*1000.0 )

        elif name in O:
            bio_w[name] = bio_w[name].apply( lambda v: v/32.0*1000.0 )
            bio_s[name] = bio_s[name].apply( lambda v: v/32.0*1000.0 )

        else:
            pass
        
    Chl2C = 0.05   # okada (=1/20 gChl/gC)
    PhyCN = 6.625  # (=106/16 molC/molN)
    ratio_CN = 8.0 # (=106/16 molC/molN)

    bio_w['phyt'] = bio_w['chlo'] / Chl2C / 12.0 / PhyCN
    bio_s['phyt'] = bio_s['chlo'] / Chl2C / 12.0 / PhyCN
    bio_w['zoop'] = bio_w['phyt'] * 0.1
    bio_s['zoop'] = bio_s['phyt'] * 0.1

    bio_w['SDeC'] = bio_w['SDeN'] * ratio_CN
    bio_s['SDeC'] = bio_s['SDeN'] * ratio_CN
    bio_w['LDeC'] = bio_w['SDeC'] * 2.0
    bio_s['LDeC'] = bio_s['SDeC'] * 2.0

    #print bio_w
    #print bio_s

    ta = len(bio_w)

    bio_out = {}
    
    for name in bio_names:
        bio_out[name] = {}
        bio_out[name]['w'] = np.ndarray(shape=[ta, s_rho, eta_rho])
        bio_out[name]['s'] = np.ndarray(shape=[ta, s_rho, xi_rho])

        for s in xrange(s_rho):
            for eta in xrange(eta_rho):
                bio_out[name]['w'][:, s, eta] = bio_w[name]
            for xi in xrange(xi_rho):
                bio_out[name]['s'][:, s, xi]  = bio_s[name]

    return bio_out, bio_w.index

if __name__ == '__main__':

    dims = {'xi':1, 'eta':1, 's':1}    
    fennelfiles = {'w':'../fennel_w.csv', 's':'../fennel_s.csv'}
    bio_out = bry_bio_fennel(dims, fennelfiles)

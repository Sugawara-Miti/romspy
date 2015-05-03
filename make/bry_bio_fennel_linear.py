# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

import numpy as np
import pandas as pd

Chl2C = 0.05   # okada (=1/20 gChl/gC)
PhyCN = 6.625  # (=106/16 molC/molN)
ratio_CN = 8.0 # (=106/16 molC/molN)
Phy2Zoo  = 0.1

def bry_bio_fennel_linear(dims, csvfiles):

    print 'bry_bio_fennel_linear:', 'w', csvfiles['w']
    print 'bry_bio_fennel_linear:', 's', csvfiles['s']

    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    s_rho   = dims['s']

    bio = {}
    bio['w'] = pd.read_csv(csvfiles['w'], skiprows=[2], parse_dates=0, index_col=0, header=[0,1])
    bio['s'] = pd.read_csv(csvfiles['s'], skiprows=[2], parse_dates=0, index_col=0, header=[0,1])
    
    for d in bio.keys():
        
        for name in bio[d].columns:
            
            if 'N' in name:
                bio[d][name] = bio[d][name].apply( lambda v: v/14.0*1000.0 )
                
            elif 'P' in name:
                bio[d][name] = bio[d][name].apply( lambda v: v/31.0*1000.0 )

            elif 'oxygen' in name:
                bio[d][name] = bio[d][name].apply( lambda v: v/32.0*1000.0 )

            else:
                pass

        for l in ['upper', 'lower']:
            bio[d]['phyt',l] = bio[d]['chlo',l] / Chl2C / 12.0 / PhyCN
            bio[d]['zoop',l] = bio[d]['phyt',l] * Phy2Zoo
            bio[d]['SDeC',l] = bio[d]['SDeN',l] * ratio_CN
            bio[d]['LDeC',l] = bio[d]['LDeN',l] * ratio_CN
            bio[d]['TIC',l]  = 2100.0
            bio[d]['TAlk',l] = 2340.0
            bio[d]['COD',l]  = 0.0
            bio[d]['H2S',l]  = 0.0

    bio_out = {}
    ta = len(bio[d])

    for name in bio[d].stack(1).columns:
        bio_out[name] = {}

        for d in bio.keys():
            if   d == 'w': length = eta_rho
            elif d == 's': length = xi_rho
            bio_out[name][d] = np.zeros([ta, s_rho, length])

            for t, index in enumerate(bio[d].index):
                upper = bio[d][name,'upper'][index]
                lower = bio[d][name,'lower'][index]
                profile = np.linspace(lower, upper, s_rho)

                for s, value in enumerate(profile):
                    bio_out[name][d][t,s,:] = value

    return bio_out, bio[d].index

if __name__ == '__main__':

    dims = {'xi':1, 'eta':1, 's':20}
    
    fennelfiles = {'w':'../fennel_w.csv', 's':'../fennel_s_linear.csv'}
    
    bio_out = bry_bio_fennel_linear(dims, fennelfiles)

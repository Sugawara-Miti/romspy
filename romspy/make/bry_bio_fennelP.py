# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

import numpy as np
import datetime as dt

Chl2C = 0.05   # okada (=1/20 gChl/gC)
PhyCN = 6.625  # (=106/16 molC/molN)
C = 12.01
N = 14.01
P = 30.97
O2 = 32.00


def bry_bio_fennelP(dims):

    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    s_rho   = dims['s']

    bionames = ['NO3', 'NH4', 'chlo', 'SDeN', 'oxygen', 'PO4', 'SDeP', 'H2S']
    dtime = [dt.datetime(2012,month,1,0,0) for month in range(1,13)]
    dtime.append(dt.datetime(2013,1,1,0,0))

    bio = {'w':{name:np.zeros(shape=[len(dtime), s_rho, eta_rho]) for name in bionames},
           's':{name:np.zeros(shape=[len(dtime), s_rho, xi_rho]) for name in bionames}}

    bio['w']['NO3'][:,:,:]     = 0.0233
    bio['s']['NO3'][:,:,:]     = 0.0326
    bio['w']['NH4'][:,:,:]     = 0.0193
    bio['s']['NH4'][:,:,:]     = 0.0104
    bio['w']['SDeN'][:,:,:]    = 0.0296  # PON
    bio['s']['SDeN'][:,:,:]    = 0.0276  # PON
    bio['w']['chlo'][:,:,:]    = 2.40
    bio['s']['chlo'][:,:,:]    = 0.788
    bio['w']['PO4'][:,:,:]     = 0.0135
    bio['s']['PO4'][:,:,:]     = 0.0123
    bio['w']['SDeP'][:,:,:]    = 0.0080  # POP
    bio['s']['SDeP'][:,:,:]    = 0.0044  # POP
    bio['w']['H2S'][:,:,:]     = 0.0
    bio['s']['H2S'][:,:,:]     = 0.0

    bio['w']['oxygen'][0,:,:]  = 8.81
    bio['w']['oxygen'][1,:,:]  = 9.40
    bio['w']['oxygen'][2,:,:]  = 9.05
    bio['w']['oxygen'][3,:,:]  = 8.6
    bio['w']['oxygen'][4,:,:]  = 7.53
    bio['w']['oxygen'][5,:,:]  = 6.52
    bio['w']['oxygen'][6,:,:]  = 5.5
    bio['w']['oxygen'][7,:,:]  = 5.45
    bio['w']['oxygen'][8,:,:]  = 5.15
    bio['w']['oxygen'][9,:,:]  = 6.44
    bio['w']['oxygen'][10,:,:] = 6.2
    bio['w']['oxygen'][11,:,:] = 7.51
    bio['w']['oxygen'][12,:,:] = 8.81
    bio['s']['oxygen'][0,:,:]  = 8.81
    bio['s']['oxygen'][1,:,:]  = 9.40
    bio['s']['oxygen'][2,:,:]  = 9.05
    bio['s']['oxygen'][3,:,:]  = 8.6
    bio['s']['oxygen'][4,:,:]  = 7.53
    bio['s']['oxygen'][5,:,:]  = 6.52
    bio['s']['oxygen'][6,:,:]  = 5.5
    bio['s']['oxygen'][7,:,:]  = 5.45
    bio['s']['oxygen'][8,:,:]  = 5.15
    bio['s']['oxygen'][9,:,:]  = 6.44
    bio['s']['oxygen'][10,:,:] = 6.2
    bio['s']['oxygen'][11,:,:] = 7.51
    bio['s']['oxygen'][12,:,:] = 8.81

    for name in bionames:

        # linear interpolation
        for t in range(len(dtime)):
            for xi in range(xi_rho):
                var = bio['s'][name]
                var[t,:,xi] = np.linspace(var[t,0,xi], var[t,-1,xi], s_rho)
            for eta in range(eta_rho):
                var = bio['w'][name]
                var[t,:,eta] = np.linspace(var[t,0,eta], var[t,-1,eta], s_rho)

        # convert unit
        for direction in ['w','s']:
            var = bio[direction][name][:,:,:]
            if 'N' in name:
                bio[direction][name] = var / N * 1000.0
            elif 'P' in name:
                bio[direction][name] = var / P * 1000.0
            elif name == 'oxygen':
                bio[direction][name] = var / O2 * 1000.0

    # copy variables
    for direction in ['w','s']:
        var = bio[direction]
        var['phyt'] = var['chlo'][:,:,:] / (Chl2C * PhyCN * C)
        var['zoop'] = var['phyt'][:,:,:] * 0.1
        var['SDeN'] = var['SDeN'][:,:,:] / 2.0
        var['SDeP'] = var['SDeP'][:,:,:] / 2.0
        var['LDeN'] = var['SDeN'][:,:,:]
        var['LDeP'] = var['SDeP'][:,:,:]

    return bio, dtime


if __name__ == '__main__':

    dims = {'xi':2, 'eta':2, 's':20}
    bio, time = bry_bio_fennelP(dims)
    print bio['w']['oxygen']

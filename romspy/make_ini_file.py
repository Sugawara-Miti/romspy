#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
2014/12/04 OKADA Teruhisa make this file.
2015/05/02 okada remake it.
"""

import datetime
import netCDF4
import numpy as np
from numpy import dtype
#import matplotlib.pyplot as plt
import pandas as pd
import itertools


def make_ini_file(grdfile, inifile, biofile=None, bgcfile=None):
    nc   = netCDF4.Dataset(grdfile, 'r')
    imax = len(nc.dimensions['xi_rho'])
    jmax = len(nc.dimensions['eta_rho'])
    kmax = 20
    Nbed = 20
    h    = nc.variables['h'][:,:]
    nc.close()

    dstart = datetime.datetime(2012,1,1,0,0,0)
    tunit_GMT = 'seconds since 1968-05-23 00:00:00 GMT'
    tunit_JST = 'seconds since 1968-05-23 09:00:00 GMT'
    time_out  = [netCDF4.date2num(dstart, tunit_JST)]

    nc = netCDF4.Dataset(inifile, 'w', format='NETCDF3_CLASSIC')
    nc.createDimension('xi_rho', imax)
    nc.createDimension('xi_u',   imax-1)
    nc.createDimension('xi_v',   imax)
    nc.createDimension('eta_rho', jmax)
    nc.createDimension('eta_u',  jmax)
    nc.createDimension('eta_v',  jmax-1)
    nc.createDimension('s_rho',  kmax)
    nc.createDimension('s_w',    kmax+1)
    nc.createDimension('ocean_time', len(time_out))

    time = nc.createVariable('ocean_time', dtype('double').char, ('ocean_time',))
    zeta = nc.createVariable('zeta', dtype('float32').char, ('ocean_time', 'eta_rho', 'xi_rho'))
    ubar = nc.createVariable('ubar', dtype('float32').char, ('ocean_time', 'eta_u', 'xi_u'))
    vbar = nc.createVariable('vbar', dtype('float32').char, ('ocean_time', 'eta_v', 'xi_v'))
    u    = nc.createVariable('u', dtype('float32').char, ('ocean_time', 's_rho', 'eta_u', 'xi_u'))
    v    = nc.createVariable('v', dtype('float32').char, ('ocean_time', 's_rho', 'eta_v', 'xi_v'))
    temp = nc.createVariable('temp', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
    salt = nc.createVariable('salt', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))

    time.units = tunit_GMT
    zeta.units = 'meter'
    ubar.units = 'meter second-1'
    vbar.units = 'meter second-1'
    u.units    = 'meter second-1'
    v.units    = 'meter second-1'
    temp.units = 'Celsius'
    salt.units = 'PSU'

    time[:]       = time_out
    zeta[:,:,:]   = 1.0
    ubar[:,:,:]   = 0.0
    vbar[:,:,:]   = 0.0
    u[:,:,:,:]    = 0.0
    v[:,:,:,:]    = 0.0
    temp[:,:,:,:] = 13.0
    salt[:,:,:,:] = 32.5

    zeta.time = 'ocean_time'
    ubar.time = 'ocean_time'
    vbar.time = 'ocean_time'
    u.time    = 'ocean_time'
    v.time    = 'ocean_time'
    temp.time = 'ocean_time'
    salt.time = 'ocean_time'

    if biofile is not None:
        add_bio(nc, biofile)

    if bgcfile is not None:
        add_bgc(nc, Nbed, h, bgcfile)

    nc.close()


def add_bio(nc, biofile):

    """
    2015/05/01 okada  All value is 0, use biofile=0
    """

    Chl2C = 0.05   # okada (=1/20 gChl/gC)
    PhyCN = 6.625  # (=106/16 molC/molN)
    C = 12.01
    N = 14.01
    P = 30.97
    O2 = 32.00

    bio_names = ['NO3','NH4','chlorophyll','phytoplankton','zooplankton',
                 'LdetritusN','SdetritusN',
                 'oxygen','PO4','LdetritusP','SdetritusP']
    bio_out = {}
    bio_out["chlorophyll"]   = 1.0
    bio_out["NO3"]           = 0.0233 / N * 1000.0
    bio_out["NH4"]           = 0.0193 / N * 1000.0
    bio_out["SdetritusN"]    = 0.0296 / N * 1000.0
    bio_out["PO4"]           = 0.0135 / P * 1000.0
    bio_out["SdetritusP"]    = 0.0080 / P * 1000.0
    bio_out["oxygen"]        = 400.0

    bio_out["phytoplankton"] = bio_out["chlorophyll"] / (Chl2C * PhyCN * C)
    bio_out["zooplankton"]   = bio_out["phytoplankton"] * 0.1
    bio_out["SdetritusN"]    = bio_out["SdetritusN"] / 2.0
    bio_out["SdetritusP"]    = bio_out["SdetritusP"] / 2.0
    bio_out["LdetritusN"]    = bio_out["SdetritusN"]
    bio_out["LdetritusP"]    = bio_out["SdetritusP"]

    nc.createDimension('bio_tracer', len(bio_names))
    bio = {}
    for name in bio_names:
        bio[name] = nc.createVariable(name, dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
    for name in bio_names:
        bio[name].units = 'milimole meter-3'
    for name in bio_names:
        bio[name][:,:,:,:] = bio_out[name]
    for name in bio_names:
        bio[name].time = 'ocean_time'
    return nc


def add_bgc(nc, Nbed, h, bgcfile):

    """
    2015/05/01 okada  Read from rst file.
    """

    bgc_names = ['O2','NH4','NO3','PO4','SO4','H2S','Mn','Fe','CH4','DOMf','DOMs',
                 'POMf','POMs','POMn','FeOOHA','FeOOHB','FeOOHP','MnO2A','MnO2B',
                 'S0','FeS','FeS2']
    bgc_out = {}
    imax = len(nc.dimensions['xi_rho'])
    jmax = len(nc.dimensions['eta_rho'])
    for name in bgc_names:
        bgc_out[name] = np.ndarray(shape=[1, Nbed, jmax, imax])
    rst1 = pd.read_csv(bgcfile.format(1))
    rst2 = pd.read_csv(bgcfile.format(2))
    print rst1.describe()

    for name in bgc_names:
        print name,
        for i, j in itertools.product(range(imax), range(jmax)):
            if 0.5 < h[j,i] < 18.0:
                bgc_out[name][0,:,j,i] = rst1[name][:Nbed]
            elif h[j,i] >= 18.0:
                bgc_out[name][0,:,j,i] = rst2[name][:Nbed]
            else:
                bgc_out[name][0,:,j,i] = 0.0
    nc.createDimension('Nbed', Nbed)
    nc.createDimension('bgc_tracer', len(bgc_names))
    bgc = {}
    for name in bgc_names:
        bgc[name] = nc.createVariable('bgc_'+name, dtype('float32').char, ('ocean_time', 'Nbed', 'eta_rho', 'xi_rho'))
    for name in bgc_names:
        bgc[name].units = 'milimole meter-3'
    for name in bgc_names:
        bgc[name][:,:,:,:] = bgc_out[name]
    for name in bgc_names:
        bgc[name].time = 'ocean_time'
    return nc

if __name__ == '__main__':

    grdfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-8.nc'
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-6.nc'
    #bgcfile = 'rst{}.csv'
    make_ini_file(grdfile, inifile, biofile=0)

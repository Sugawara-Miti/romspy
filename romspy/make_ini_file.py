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

    """Cs_w_out  = [-1.0,-0.85995970425573898,-0.73930480862785297,-0.63531548401717497,-0.54564758027872295,-0.46827978387540298,-0.40146805298528299,-0.34370630292862198,-0.29369245567696201,-0.25029908812485502,-0.21254801747113999,-0.179588250807868,-0.15067680185167201,-0.125161942384141,-0.10246851085149,-0.082084946946771098,-0.063551759905316196,-0.046451170563227499,-0.030397693687904299,-0.015029448285449901,0.0]
    #Cs_r_out  = [-0.927370400041031,-0.79738854970395501,-0.68538160680467097,-0.58882468628964602,-0.50554118089585998,-0.43365369559286598,-0.37154172693258403,-0.31780513330542598,-0.27123257264129702,-0.230774196071171,-0.19551798200381801,-0.16466917713521501,-0.137532380945393,-0.11349586982752299,-0.0920178074803049,-0.072614030715317204,-0.054847135344321701,-0.038316616118190899,-0.022649838449810701,-0.0074936384035539797]
    #s_w_out   = [-1.0 + float(k)/kmax for k in range(kmax+1)]
    #s_rho_out = [(s_w_out[k] + s_w_out[k+1])/2 for k in range(kmax)]"""
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
    # nc.createDimension('frc_adjust', 2)
    # nc.createDimension('obc_adjust', 2)
    # nc.createDimension('boundary',   4)
    # nc.createDimension('IorJ',       max(imax,jmax))

    """spherical = nc.createVariable('spherical', dtype('int32').char)
    #theta_s   = nc.createVariable('theta_s', dtype('double').char)
    #theta_b   = nc.createVariable('theta_b', dtype('double').char)
    #Tcline    = nc.createVariable('Tcline', dtype('double').char)
    #hc        = nc.createVariable('hc', dtype('double').char)
    #s_rho     = nc.createVariable('s_rho', dtype('double').char, ('s_rho',))
    #s_w       = nc.createVariable('s_w', dtype('double').char, ('s_w',))
    #Cs_r      = nc.createVariable('Cs_r', dtype('double').char, ('s_rho',))
    #Cs_w      = nc.createVariable('Cs_w', dtype('double').char, ('s_w',))"""

    time = nc.createVariable('ocean_time', dtype('double').char, ('ocean_time',))
    zeta = nc.createVariable('zeta', dtype('float32').char, ('ocean_time', 'eta_rho', 'xi_rho'))
    ubar = nc.createVariable('ubar', dtype('float32').char, ('ocean_time', 'eta_u', 'xi_u'))
    vbar = nc.createVariable('vbar', dtype('float32').char, ('ocean_time', 'eta_v', 'xi_v'))
    u    = nc.createVariable('u', dtype('float32').char, ('ocean_time', 's_rho', 'eta_u', 'xi_u'))
    v    = nc.createVariable('v', dtype('float32').char, ('ocean_time', 's_rho', 'eta_v', 'xi_v'))
    temp = nc.createVariable('temp', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
    salt = nc.createVariable('salt', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))

    """spherical.flag_values = [0, 1]
    theta_s.units   = 'nondimensional'
    theta_b.units   = 'nondimensional'
    Tcline.units    = 'meter'
    hc.units        = 'meter'
    s_rho.units     = 'nondimensional'
    s_w.units       = 'nondimensional'
    Cs_r.units      = 'nondimensional'
    Cs_w.units      = 'nondimensional'"""

    time.units = tunit_GMT
    zeta.units = 'meter'
    ubar.units = 'meter second-1'
    vbar.units = 'meter second-1'
    u.units    = 'meter second-1'
    v.units    = 'meter second-1'
    temp.units = 'Celsius'
    salt.units = 'PSU'

    """spherical[:] = 1
    theta_s[:]      = 3
    theta_b[:]      = 0
    Tcline[:]       = 0.5
    hc[:]           = 0.5
    s_rho[:]       = s_rho_out
    s_w[:]         = s_w_out
    Cs_r[:]        = Cs_r_out
    Cs_w[:]        = Cs_w_out"""

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
        add_bgc(nc, Nbed, bgcfile)

    nc.close()


def add_bio(nc, biofile):

    """
    2015/05/01 okada  All value is 0, use biofile=0
    """

    Chl2C_m = 0.0535  #[mg_Chl/mg_C]
    ChlMin = 0.001  #[mg_Chl/m3]
    PhyPN = 0.08  #[mole_P/mole_N]
    PhyCN = 6.625  #[mole_C/mole_N]

    bio_names = ['NO3','NH4','chlorophyll','phytoplankton','zooplankton',
                 'LdetritusN','SdetritusN',
                 'oxygen','PO4','LdetritusP','SdetritusP']
    bio_out = {}
    bio_out["NO3"] = 10.0
    bio_out["NH4"] = 0.1
    bio_out["chlorophyll"] = 1.0
    bio_out["phytoplankton"] = bio_out["chlorophyll"]/Chl2C_m/12/PhyCN
    bio_out["zooplankton"] = bio_out["phytoplankton"]/2
    bio_out["LdetritusN"] = bio_out["phytoplankton"]
    bio_out["SdetritusN"] = bio_out["phytoplankton"]
    bio_out["oxygen"] = 200.0
    bio_out["PO4"] = 1.0
    bio_out["LdetritusP"] = bio_out["LdetritusN"]*PhyPN
    bio_out["SdetritusP"] = bio_out["SdetritusN"]*PhyPN

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


def add_bgc(nc, Nbed, bgcfile):

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

    grdfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-6.nc'
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-2.nc'
    #bgcfile = 'rst{}.csv'
    make_ini_file(grdfile, inifile, biofile=0)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
2014/12/04 OKADA Teruhisa make this file.
2015/05/02 okada remake it.
"""

from datetime import datetime
import netCDF4
from numpy import dtype


def make_ini_file(grdfile, inifile, biofile=None, bgcfile=None, dstart=datetime(2012,1,1,0,0,0)):

    kmax = 20
    Nbed = 20

    nc   = netCDF4.Dataset(grdfile, 'r')
    imax = len(nc.dimensions['xi_rho'])
    jmax = len(nc.dimensions['eta_rho'])
    lon = nc.variables['lon_rho'][:,:]
    lat = nc.variables['lat_rho'][:,:]
    h   = nc.variables['h'][:,:]
    nc.close()

    GMT = 'seconds since 1968-05-23 00:00:00 GMT'
    JST = 'seconds since 1968-05-23 09:00:00 GMT'
    time_out  = [netCDF4.date2num(dstart, JST)]

    nc = netCDF4.Dataset(inifile, 'w', format='NETCDF3_CLASSIC')
    nc.Author = 'romspy.make_ini_file'
    nc.Created = datetime.now().isoformat()
    nc.grdfile = grdfile

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
    lon_rho = nc.createVariable('lon_rho', dtype('float32').char, ('eta_rho', 'xi_rho'))
    lat_rho = nc.createVariable('lat_rho', dtype('float32').char, ('eta_rho', 'xi_rho'))
    zeta = nc.createVariable('zeta', dtype('float32').char, ('ocean_time', 'eta_rho', 'xi_rho'))
    ubar = nc.createVariable('ubar', dtype('float32').char, ('ocean_time', 'eta_u', 'xi_u'))
    vbar = nc.createVariable('vbar', dtype('float32').char, ('ocean_time', 'eta_v', 'xi_v'))
    u    = nc.createVariable('u', dtype('float32').char, ('ocean_time', 's_rho', 'eta_u', 'xi_u'))
    v    = nc.createVariable('v', dtype('float32').char, ('ocean_time', 's_rho', 'eta_v', 'xi_v'))
    temp = nc.createVariable('temp', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
    salt = nc.createVariable('salt', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))

    time.units = GMT
    lon_rho.units = 'degree_north'
    lat_rho.units = 'degree_east'
    zeta.units = 'meter'
    ubar.units = 'meter second-1'
    vbar.units = 'meter second-1'
    u.units    = 'meter second-1'
    v.units    = 'meter second-1'
    temp.units = 'Celsius'
    salt.units = 'PSU'

    time[:]       = time_out
    lon_rho[:,:]  = lon
    lat_rho[:,:]  = lat
    zeta[:,:,:]   = 0.0  # 1.5
    ubar[:,:,:]   = 0.0
    vbar[:,:,:]   = 0.0
    u[:,:,:,:]    = 0.0
    v[:,:,:,:]    = 0.0
    temp[:,:,:,:] = 0.0  # 13.0
    salt[:,:,:,:] = 0.0  # 32.5

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
    bio_out["chlorophyll"]   = 0.0  # 1.0
    bio_out["NO3"]           = 0.0  # 0.0233 / N * 1000.0
    bio_out["NH4"]           = 0.0  # 0.0193 / N * 1000.0
    bio_out["SdetritusN"]    = 0.0  # 0.0296 / N * 1000.0
    bio_out["PO4"]           = 0.0  # 0.0135 / P * 1000.0
    bio_out["SdetritusP"]    = 0.0  # 0.0080 / P * 1000.0
    bio_out["oxygen"]        = 0.0  # 400.0

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


if __name__ == '__main__':

    grdfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-8.nc'
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_zero_0805.nc'
    #bgcfile = 'rst{}.csv'
    make_ini_file(grdfile, inifile, biofile=0, dstart=datetime(2012,8,5,0,0,0))

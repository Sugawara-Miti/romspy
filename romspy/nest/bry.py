# -*- coding: utf-8 -*-

"""
2015/05/01 okada   make this file versio is 2.0
"""

import datetime
import netCDF4
import numpy as np
from numpy import dtype
import pandas as pd

#from make import *

__version__ = 3.0
bio_units = {'others':'millimole meter-3',
             'chlorophyll':'milligram meter-3',
             'alkalinity':'milliequivalens meter-3'}


def bry_time(dates=['2012-1-1', '2013-1-1'], bio_index=None):

    tunit_JST = 'days since 1968-05-23 09:00:00 GMT'

    time_h = pd.date_range(dates[0], dates[1], freq='H').to_pydatetime()
    time_d = pd.date_range(dates[0], dates[1], freq='D').to_pydatetime()
    time_a = [time_d[0], time_d[-1]]
    if bio_index is not None:
        #time_b = bio_index.to_pydatetime()
        time_b = bio_index
    time_out = {}
    time_out['time_hourly']   = netCDF4.date2num(time_h, tunit_JST)
    time_out['time_daily']    = netCDF4.date2num(time_d, tunit_JST)
    time_out['time_annually'] = netCDF4.date2num(time_a, tunit_JST)
    if bio_index is not None:
        time_out['time_biology'] = netCDF4.date2num(time_b, tunit_JST)

    print time_out
    return time_out


def bry_write_time(nc, time_out):

    tunit_GMT = 'days since 1968-05-23 00:00:00 GMT'

    time = {}
    for name in time_out.keys():

        print 'bry_write_time:',name

        nc.createDimension(name, len(time_out[name]))
        time[name] = nc.createVariable(name, dtype('double').char, (name,))
        time[name].units = tunit_GMT
        time[name][:] = time_out[name]


def bry_write_2d(nc, vname, var_out, timename, p, units):

    print 'bry_write_2d:', vname

    var = {}
    for d in var_out.keys():
        if d == 'w':
            var['w'] = nc.createVariable('{}_west'.format(vname),  dtype('float32').char, (timename,'eta_{}'.format(p)))
        elif d == 's':
            var['s'] = nc.createVariable('{}_south'.format(vname), dtype('float32').char, (timename,'xi_{}'.format(p)))
        else:
            return
        var[d].units = units
        print d, var[d].shape, var_out[d].shape
        var[d][0,:]  = var_out[d]
        var[d][-1,:]  = var_out[d]
        var[d].time  = timename


def bry_write_3d(nc, vname, var_out, timename, p, units):

    print 'bry_write_3d:', vname

    var = {}
    for d in var_out.keys():
        if d == 'w':
            var['w'] = nc.createVariable('{}_west'.format(vname),  dtype('float32').char, (timename,'s_rho','eta_{}'.format(p)))
        elif d == 's':
            var['s'] = nc.createVariable('{}_south'.format(vname), dtype('float32').char, (timename,'s_rho','xi_{}'.format(p)))
        else:
            return
        var[d].units   = units
        var[d][0,:,:]  = var_out[d]
        var[d][-1,:,:] = var_out[d]
        var[d].time    = timename


def ini2bry(ncfile, dims, dates, inifile):

    xi = dims['xi'][0]-1
    xi_u = xi
    xi_v = xi
    eta = np.arange(dims['eta'][0]-1, dims['eta'][1], 1)
    eta_u = eta[:]
    eta_v = eta[:-1]

    ini = netCDF4.Dataset(inifile, 'r')
    zeta = ini.variables['zeta'][0,eta,xi]
    print zeta.shape
    ubar = ini.variables['ubar'][0,eta_u,xi_u]
    vbar = ini.variables['vbar'][0,eta_v,xi_v]
    u = ini.variables['u'][0,:,eta_u,xi_u]
    v = ini.variables['v'][0,:,eta_v,xi_v]
    temp = ini.variables['temp'][0,:,eta,xi]
    salt = ini.variables['salt'][0,:,eta,xi]

    bionames = ['NH4', 'NO3', 'chlorophyll', 'phytoplankton', 'zooplankton', 'LdetritusN', 'SdetritusN', 'oxygen', 'PO4', 'LdetritusP', 'SdetritusP']
    bio = {}
    for name in bionames:
        bio[name] = ini.variables[name][0,:,eta,xi]
    ini.variables

    time_out = bry_time(dates)

    # write
    nc = netCDF4.Dataset(ncfile, 'w', format='NETCDF3_CLASSIC') 
    now = datetime.datetime.now()
    nc.history = now.strftime('%Y-%m-%d %H:%M:%S')
    nc.author = 'OKADA Teruhisa'
    nc.createDimension('eta_rho', len(eta))
    nc.createDimension('eta_u',   len(eta_u))
    nc.createDimension('eta_v',   len(eta_v))
    nc.createDimension('s_rho',   dims['s'])

    # write time
    bry_write_time(nc, time_out)

    # write variables
    bry_write_2d(nc, 'zeta', {'w':zeta}, 'time_annually', 'rho', 'meter')  
    bry_write_2d(nc, 'ubar', {'w':ubar}, 'time_annually', 'u', 'meter second-1')
    bry_write_2d(nc, 'vbar', {'w':vbar}, 'time_annually', 'v', 'meter second-1')
    bry_write_3d(nc, 'u',    {'w':u}, 'time_annually', 'u', 'meter second-1')
    bry_write_3d(nc, 'v',    {'w':v}, 'time_annually', 'v', 'meter second-1')
    bry_write_3d(nc, 'temp', {'w':temp}, 'time_annually', 'rho', 'Celsius')
    bry_write_3d(nc, 'salt', {'w':salt}, 'time_annually', 'rho', 'PSU')

    short = {'LdetritusP':'LDeP','SdetritusP':'SDeP','SdetritusN':'SDeN','LdetritusN':'LDeN'}
    for name in bionames:
        units = bio_units[name] if name in bio_units else bio_units['others']
        if name in short.keys():
            vname = short[name]
        elif len(name) > 6:
            vname = name[:4]
        else:
            vname = name
        bry_write_3d(nc, vname, {'w':bio[name]}, 'time_annually', 'rho', units)

    nc.close()


def _test1():

    ncfile = '/Users/teruhisa/Dropbox/Data/ob500a_bry_2012_fennelP-1.nc'

    dims = {'xi':[58], 'eta':[35,124], 's':20}
    dates = ['2012-01-01', '2013-01-01']
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_NL05_0805.nc'

    ini2bry(ncfile, dims, dates, inifile=inifile)


if __name__ == '__main__':

    _test1()

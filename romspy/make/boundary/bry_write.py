# coding: utf-8
# (c) 2015-10-14 Teruhisa Okada
# 2014/10/21 1.0
# 2015/10/14 2.0

from numpy import dtype
import netCDF4
import datetime

__version__ = 2.0

JST = 'days since 1968-05-23 09:00:00 GMT'
GMT = 'days since 1968-05-23 00:00:00 GMT'


def bry_write_time(nc, name, time_out):

    print 'bry_write_time:',name

    nc.createDimension(name, len(time_out))
    time = nc.createVariable(name, dtype('double').char, (name,))
    time.units = GMT
    if type(time_out[0]) == datetime.datetime:
        time[:] = netCDF4.date2num(time_out, JST)
    else:
        time[:] = time_out


def bry_write_2d(nc, vname, var_out, timename, p, units):

    print 'bry_write_2d:', vname

    var = {}
    var['w'] = nc.createVariable('{}_west'.format(vname),  dtype('float32').char, (timename,'eta_{}'.format(p)))
    var['s'] = nc.createVariable('{}_south'.format(vname), dtype('float32').char, (timename,'xi_{}'.format(p)))
    for d in var_out.keys():
        var[d].units = units
        var[d][:,:]  = var_out[d]
        var[d].time  = timename


def bry_write_3d(nc, vname, var_out, timename, p, units):

    print 'bry_write_3d:', vname

    var = {}
    var['w'] = nc.createVariable('{}_west'.format(vname),  dtype('float32').char, (timename,'s_rho','eta_{}'.format(p)))
    var['s'] = nc.createVariable('{}_south'.format(vname), dtype('float32').char, (timename,'s_rho','xi_{}'.format(p)))
    for d in var_out.keys():
        var[d].units   = units
        var[d][:,:,:]  = var_out[d]
        var[d].time    = timename

# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

from numpy import dtype


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
        var[d][:,:]  = var_out[d]
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
        var[d][:,:,:]  = var_out[d]
        var[d].time    = timename

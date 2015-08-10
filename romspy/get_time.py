# -*- coding: utf-8 -*-

"""
2015-08-01 okada  
"""

import netCDF4

JST = 'seconds since 1968-05-23 09:00:00 GMT'


def get_time(ncfile, which='ends', tunit=JST, name='ocean_time'):
    nc = netCDF4.Dataset(ncfile, 'r')
    print ncfile
    if which == 'ends':
        t = len(nc.dimensions[name])
        start = nc.variables[name][0]
        end = nc.variables[name][t-1]
        print netCDF4.num2date(start, tunit), 0
        print netCDF4.num2date(end, tunit), t-1
    elif which == 'all':
        time = nc.variables[name][:]
        for t in range(len(time)):
            print netCDF4.num2date(time[t], JST), t
    else:
        print 'You should select "ends" or "all"'
    nc.close()

if __name__ == '__main__':
    #import romspy
    get_time('/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-6.nc')

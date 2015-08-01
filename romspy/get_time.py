# -*- coding: utf-8 -*-

"""
2015-08-01 okada  
"""

import netCDF4


def get_time(ncfile):
    JST = 'seconds since 1968-05-23 09:00:00 GMT'
    nc = netCDF4.Dataset(ncfile, 'r')
    time = nc.variables['ocean_time'][:]
    print ncfile
    print netCDF4.num2date(time[0], JST), 0
    print netCDF4.num2date(time[-1], JST), len(time[:])-1

if __name__ == '__main__':
    #import romspy
    get_time('/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-6.nc')

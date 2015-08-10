# -*- coding: utf-8 -*-

"""
2015-08-04 okada  
"""

import netCDF4

JST = 'seconds since 1968-05-23 09:00:00 GMT'


def get_variables(ncfile):
    nc = netCDF4.Dataset(ncfile, 'r')
    print ncfile
    print nc.variables.keys()
    nc.close()

if __name__ == '__main__':
    #import romspy
    get_time('/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-6.nc')

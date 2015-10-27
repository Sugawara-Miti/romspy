# coding: utf-8
# (c) 2015-08-04 Teruhisa Okada  

import netCDF4

__version__ = 0.1  # 2015-10-27


def get_vnames(ncfile):
    nc = netCDF4.Dataset(ncfile, 'r')
    print ncfile
    print nc.variables.keys()
    nc.close()

if __name__ == '__main__':
    get_vnames('/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-6.nc')

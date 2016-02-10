# coding: utf-8
# (c) 2015-11-19 Teruhisa Okada

import netCDF4


def get_dim(ncfile):

    nc = netCDF4.Dataset(ncfile, 'r')
    return nc.dimensions

if __name__ == '__main__':
    ncfile = 'F:/okada/Dropbox/Data/ob500_grd-10.nc'
    dims = get_dim(ncfile)
    print dims['xi_rho']
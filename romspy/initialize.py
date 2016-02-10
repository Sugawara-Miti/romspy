# coding: utf-8
# (c) 2015 Teruhisa Okada

import datetime
import netCDF4

"""
def initialize(inifile, date, vname, value):
    day = datetime.datetime.strftime(date, '%m%d')
    inifile = inifile.format(day)
    print inifile, vname, '=>', value 

    ini = netCDF4.Dataset(inifile, 'r+', format='NETCDF3_CLASSIC')
    var = ini.variables[vname]
    if var.ndim == 3:
        var[0,:,:] = value
    elif var.ndim == 4:
        var[0,:,:,:] = value
    ini.close()"""


def initialize(ncfile, vname, value, date=None):
    if date is not None:
        day = datetime.datetime.strftime(date, '%m%d')
        ncfile = ncfile.format(day)
    print ncfile, vname, '=>', value 

    nc = netCDF4.Dataset(ncfile, 'r+', format='NETCDF3_CLASSIC')
    var = nc[vname]
    if var.ndim == 1:
        var[:] = value
    elif var.ndim == 2:
        var[:,:] = value
    elif var.ndim == 3:
        var[0,:,:] = value
    elif var.ndim == 4:
        var[0,:,:,:] = value
    nc.close()

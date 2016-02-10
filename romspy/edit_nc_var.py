# coding: utf-8
# (c) 2015-11-23 Teruhisa Okada

import netCDF4
import datetime


def edit_nc_var(ncfile, varname, value, t=None):
    nc = netCDF4.Dataset(ncfile, 'r+')
    nc.Author = 'Teruhisa Okada'
    nc.Edited = datetime.datetime.now().isoformat()

    if varname in nc.variables.keys():
        print ncfile, varname
        var = nc.variables[varname]
        if var.ndim == 3:
            if t is not None:
                var[:,:,:] = value
            else:
                var[t,:,:] = value
        elif var.ndim == 4:
            if t is not None:
                var[t,:,:,:] = value
            else:
                var[:,:,:,:] = value
    else:
        print "ERROR: {} don't exist in {}.".format(varname, ncfile)
    nc.close()

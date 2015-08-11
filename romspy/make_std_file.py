# coding: utf-8

import netCDF4
import numpy as np
import shutil
from datetime import datetime


def edit_var(ncfile, varname, values):
    nc = netCDF4.Dataset(ncfile, 'r+')
    nc.Author = 'romspy.make_std_file.edit_var'
    nc.Created = datetime.now().isoformat()

    if varname in nc.variables.keys():
        print varname
        var = nc.variables[varname]
        if var.ndim == 3:
            var[:,:,:] = values
        elif var.ndim == 4:
            profile = np.linspace(values[0], values[1], 20)
            for k in range(20):
                var[:,k,:,:] = profile[k]
    else:
        print varname, "don't exist in this initial file."
    nc.close()


def make_std_file(inifile, stdfile):
    shutil.copyfile(inifile, stdfile)
    edit_var(stdfile, 'zeta', 0.0)
    edit_var(stdfile, 'ubar', 0.0)
    edit_var(stdfile, 'vbar', 0.0)
    edit_var(stdfile, 'u', [0.0, 0.0])
    edit_var(stdfile, 'v', [0.0, 0.0])
    edit_var(stdfile, 'temp', [0.0, 1.0])
    edit_var(stdfile, 'salt', [0.0, 1.0])
    edit_var(stdfile, 'NO3', [0.0, 1.0])
    edit_var(stdfile, 'NH4', [0.0, 0.1])
    edit_var(stdfile, 'chlorophyll', [0.0, 3.0])
    edit_var(stdfile, 'phytoplankton', [0.0, 0.5])
    edit_var(stdfile, 'zooplankton', [0.0, 0.05])
    edit_var(stdfile, 'LdetritusN', [0.0, 1.0])
    edit_var(stdfile, 'SdetritusN', [0.0, 1.0])
    edit_var(stdfile, 'oxygen', [0.0, 50.0])
    edit_var(stdfile, 'PO4', [0.0, 0.1])
    edit_var(stdfile, 'LdetritusP', [0.0, 0.1])
    edit_var(stdfile, 'SdetritusP', [0.0, 0.1])
    edit_var(stdfile, 'H2S', [0.0, 0.0])


if __name__ == '__main__':
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-7.nc'
    stdfile = '/Users/teruhisa/Dropbox/Data/ob500_std_i_fennelP-3.nc'
    make_std_file(inifile, stdfile)

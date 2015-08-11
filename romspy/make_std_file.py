# coding: utf-8

import netCDF4
import numpy as np
import shutil
import datetime


def edit_var(ncfile, varname, values):
    nc = netCDF4.Dataset(ncfile, 'r+')
    nc.Author = 'romspy.make_std_file'
    nc.Created = datetime.now().isoformat()

    if varname in nc.variables.keys():
        var = nc.variables[varname]
        profile = np.linspace(values[1], values[20])
        for k in range(20):
            var[:,k,:,:] = profile[k]
        print varname
    else:
        print varname, "don't exist in this initial file."
    nc.close()


def make_std_file():
    shutil.copyfile(inifile, stdfile)
    edit_var(stdfile, 'temp', {20:1.0, 1:0.0})
    edit_var(stdfile, 'salt', {20:1.0, 1:0.0})
    edit_var(stdfile, 'NO3', {20:1.0, 1:0.0})
    edit_var(stdfile, 'NH4', {20:0.1, 1:0.0})
    edit_var(stdfile, 'chlorophyll', {20:1.0, 1:0.0})
    edit_var(stdfile, 'phytoplankton', {20:0.1, 1:0.0})
    edit_var(stdfile, 'zooplankton', {20:0.1, 1:0.0})
    edit_var(stdfile, 'LdetritusN', {20:1.0, 1:0.0})
    edit_var(stdfile, 'SdetritusN', {20:1.0, 1:0.0})
    edit_var(stdfile, 'oxygen', {20:1.0, 1:0.0})
    edit_var(stdfile, 'PO4', {20:1.0, 1:0.0})
    edit_var(stdfile, 'LdetritusP', {20:1.0, 1:0.0})
    edit_var(stdfile, 'SdetritusP', {20:1.0, 1:0.0})
    edit_var(stdfile, 'H2S', {20:1.0, 1:0.0})


if __name__ == '__main__':
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-1.nc'
    stdfile = '/Users/teruhisa/Dropbox/Data/ob500_std_i_fennelP-1.nc'
    make_std_file(inifile, stdfile)

# coding: utf-8

import netCDF4
import numpy as np
import shutil


def edit_variable(ncfile, varname, values):
    nc = netCDF4.Dataset(ncfile, 'r+')
    if varname in nc.variables.keys():
        var = nc.variables[varname]
        profile = np.linspace(values[1], values[20])
        for k in range(20):
            var[:,k,:,:] = profile[k]
        print varname
    else:
        print varname, "don't exist in this initial file."
    nc.close()


if __name__ == '__main__':
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_fennelP-1.nc'
    stdfile = '/Users/teruhisa/Dropbox/Data/ob500_std_i_fennelP-1.nc'
    shutil.copyfile(inifile, stdfile)
    edit_variable(stdfile, 'temp', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'salt', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'NO3', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'NH4', {20:0.1, 1:0.0})
    edit_variable(stdfile, 'chlorophyll', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'phytoplankton', {20:0.1, 1:0.0})
    edit_variable(stdfile, 'zooplankton', {20:0.1, 1:0.0})
    edit_variable(stdfile, 'LdetritusN', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'SdetritusN', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'oxygen', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'PO4', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'LdetritusP', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'SdetritusP', {20:1.0, 1:0.0})
    edit_variable(stdfile, 'H2S', {20:1.0, 1:0.0})

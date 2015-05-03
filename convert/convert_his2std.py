# -*- coding:utf-8 -*-

import shutil
import netCDF4
import numpy as np

hisfile = '/home/work/okada/bio_toy/ocean_his.nc'
rstfile = '/home/work/okada/bio_toy/ocean_rst.nc'
stdfile = '/home/work/okada/bio_toy/bio_toy_std_i.nc'
shutil.copyfile(rstfile, stdfile)

his = netCDF4.Dataset(hisfile, 'r', format='NETCDF3_CLASSIC')
std = netCDF4.Dataset(stdfile, 'a', format='NETCDF3_CLASSIC')

zeta = his.variables['zeta'][:,:,:]
ubar = his.variables['ubar'][:,:,:]
vbar = his.variables['vbar'][:,:,:]
u = his.variables['u'][:,:,:,:]
v = his.variables['v'][:,:,:,:]
temp = his.variables['temp'][:,:,:,:]
salt = his.variables['salt'][:,:,:,:]
NO3  = his.variables['NO3'][:,:,:,:]
phyt = his.variables['phytoplankton'][:,:,:,:]
zoop = his.variables['zooplankton'][:,:,:,:]
detr = his.variables['detritus'][:,:,:,:]

his.close()

for t in range(len(std.dimensions['ocean_time'])):
    std.variables['zeta'][t,:,:] = np.std(zeta, axis=0)
    std.variables['ubar'][t,:,:] = np.std(ubar, axis=0)
    std.variables['vbar'][t,:,:] = np.std(vbar, axis=0)
    std.variables['u'][t,:,:,:] = np.std(u, axis=0)
    std.variables['v'][t,:,:,:] = np.std(v, axis=0)
    std.variables['temp'][t,:,:,:] = np.std(temp, axis=0)
    std.variables['salt'][t,:,:,:] = np.std(salt, axis=0)
    std.variables['NO3'][t,:,:,:] = np.std(NO3, axis=0)
    std.variables['phytoplankton'][t,:,:,:] = np.std(phyt, axis=0)
    std.variables['zooplankton'][t,:,:,:] = np.std(zoop, axis=0)
    std.variables['detritus'][t,:,:,:] = np.std(detr, axis=0)

std.close()

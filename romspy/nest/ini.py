# -*- coding: utf-8 -*-

import netCDF4
import numpy as np
from numpy import dtype


def ini(oldfile, newfile, xi, eta):

    xi = np.arange(xi[0]-1, xi[1], 1)
    eta = np.arange(eta[0]-1, eta[1], 1)
    xi_rho = len(xi)
    eta_rho = len(eta)
    print xi_rho, xi
    print eta_rho, eta

    GMT = 'seconds since 1968-05-23 00:00:00 GMT'

    old = netCDF4.Dataset(oldfile, 'r')
    new = netCDF4.Dataset(newfile, 'w', format='NETCDF3_CLASSIC')

    new.createDimension("xi_rho", xi_rho)
    new.createDimension("xi_u", xi_rho-1)
    new.createDimension("xi_v", xi_rho)

    new.createDimension("eta_rho", eta_rho)
    new.createDimension("eta_u", eta_rho)
    new.createDimension("eta_v", eta_rho-1)

    new.createDimension("s_rho", len(old.dimensions["s_rho"]))
    new.createDimension("ocean_time", None)

    time = new.createVariable('ocean_time', dtype('double').char, ('ocean_time',))
    lon  = new.createVariable('lon_rho', dtype('float32').char, ('eta_rho', 'xi_rho'))
    lat  = new.createVariable('lat_rho', dtype('float32').char, ('eta_rho', 'xi_rho'))
    zeta = new.createVariable('zeta', dtype('float32').char, ('ocean_time', 'eta_rho', 'xi_rho'))
    ubar = new.createVariable('ubar', dtype('float32').char, ('ocean_time', 'eta_u', 'xi_u'))
    vbar = new.createVariable('vbar', dtype('float32').char, ('ocean_time', 'eta_v', 'xi_v'))
    u    = new.createVariable('u', dtype('float32').char, ('ocean_time', 's_rho', 'eta_u', 'xi_u'))
    v    = new.createVariable('v', dtype('float32').char, ('ocean_time', 's_rho', 'eta_v', 'xi_v'))
    temp = new.createVariable('temp', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
    salt = new.createVariable('salt', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))

    time.units = GMT
    lon.units  = "degree_north"
    lat.units  = "degree_north"
    zeta.units = 'meter'
    ubar.units = 'meter second-1'
    vbar.units = 'meter second-1'
    u.units    = 'meter second-1'
    v.units    = 'meter second-1'
    temp.units = 'Celsius'
    salt.units = 'PSU'

    time[:]     = old.variables['ocean_time'][:]
    lon[:,:]    = old.variables['lon_rho'][eta,xi]
    lat[:,:]    = old.variables['lat_rho'][eta,xi]
    zeta[:,:,:] = old.variables['zeta'][:,eta,xi]
    ubar[:,:,:] = old.variables['ubar'][:,eta,xi[0]:xi[-1]]
    vbar[:,:,:] = old.variables['vbar'][:,eta[0]:eta[-1], xi]
    u[:,:,:,:]  = old.variables['u'][:,:,eta,xi[0]:xi[-1]]
    v[:,:,:,:]  = old.variables['v'][:,:,eta[0]:eta[-1], xi]
    temp[:,:,:,:] = old.variables['temp'][:,:,eta,xi]
    salt[:,:,:,:] = old.variables['salt'][:,:,eta,xi]

    zeta.time = 'ocean_time'
    ubar.time = 'ocean_time'
    vbar.time = 'ocean_time'
    u.time    = 'ocean_time'
    v.time    = 'ocean_time'
    temp.time = 'ocean_time'
    salt.time = 'ocean_time'

    _add_bio(old, new, eta, xi)

    old.close()
    new.close()


def _add_bio(old, new, eta, xi):

    bio_names = ['NO3','NH4','chlorophyll','phytoplankton','zooplankton',
                 'LdetritusN','SdetritusN',
                 'oxygen','PO4','LdetritusP','SdetritusP']
    new.createDimension('bio_tracer', len(bio_names))
    bio = {}
    for name in bio_names:
        print name
        bio[name] = new.createVariable(name, dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
        bio[name].units = 'milimole meter-3'
        bio[name][:,:,:,:] = old.variables[name][:,:,eta,xi]
        bio[name].time = 'ocean_time'
    return new


if __name__ == '__main__':

    oldfile = '/Users/teruhisa/Dropbox/Data/ob500_ini_NL05_0805.nc'
    newfile = '/Users/teruhisa/Dropbox/Data/ob500a_ini_NL05_0805.nc'

    ini(oldfile, newfile, xi=[58,117], eta=[35,124])

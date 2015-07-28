# -*- coding: utf-8 -*-

import netCDF4
import datetime
import numpy as np
from numpy import dtype


def make_his2ini(hisfile, inifile, dstart):

    tunit_GMT = 'days since 1968-05-23 00:00:00 GMT'
    tunit_JST = 'days since 1968-05-23 09:00:00 GMT'

    his = netCDF4.Dataset(hisfile, 'r')
    ini = netCDF4.Dataset(inifile, 'w', format='NETCDF3_CLASSIC')

    time = his.variables['ocean_time']
    dstart = netCDF4.date2num(dstart, tunit_JST)
    t = np.where(time[:]==dstart)[0][0]

    for name in his.dimensions.keys():
        if name == 'ocean_time':
            ini.createDimension(name, 1)
        else:
            ini.createDimension(name, len(his.dimensions[name]))

    time = ini.createVariable('ocean_time', dtype('double').char, ('ocean_time',))
    zeta = ini.createVariable('zeta', dtype('float32').char, ('ocean_time', 'eta_rho', 'xi_rho'))
    ubar = ini.createVariable('ubar', dtype('float32').char, ('ocean_time', 'eta_u', 'xi_u'))
    vbar = ini.createVariable('vbar', dtype('float32').char, ('ocean_time', 'eta_v', 'xi_v'))
    u    = ini.createVariable('u', dtype('float32').char, ('ocean_time', 's_rho', 'eta_u', 'xi_u'))
    v    = ini.createVariable('v', dtype('float32').char, ('ocean_time', 's_rho', 'eta_v', 'xi_v'))
    temp = ini.createVariable('temp', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
    salt = ini.createVariable('salt', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))

    time.units = tunit_GMT
    zeta.units = 'meter'
    ubar.units = 'meter second-1'
    vbar.units = 'meter second-1'
    u.units    = 'meter second-1'
    v.units    = 'meter second-1'
    temp.units = 'Celsius'
    salt.units = 'PSU'

    time[:]     = his.variables['ocean_time'][t]
    zeta[:,:,:] = his.variables['zeta'][t,:,:]
    ubar[:,:,:] = his.variables['ubar'][t,:,:]
    vbar[:,:,:] = his.variables['vbar'][t,:,:]
    u[:,:,:,:]  = his.variables['u'][t,:,:,:]
    v[:,:,:,:]  = his.variables['v'][t,:,:,:]
    temp[:,:,:,:] = his.variables['temp'][t,:,:,:]
    salt[:,:,:,:] = his.variables['salt'][t,:,:,:]

    zeta.time = 'ocean_time'
    ubar.time = 'ocean_time'
    vbar.time = 'ocean_time'
    u.time    = 'ocean_time'
    v.time    = 'ocean_time'
    temp.time = 'ocean_time'
    salt.time = 'ocean_time'

    add_bio(ini, his, t)

    ini.close()
    his.close()


def add_bio(ini, his, t):

    bio_names = ['NO3','NH4','chlorophyll','phytoplankton','zooplankton',
                 'LdetritusN','SdetritusN',
                 'oxygen','PO4','LdetritusP','SdetritusP']
    ini.createDimension('bio_tracer', len(bio_names))
    bio = {}
    for name in bio_names:
        bio[name] = ini.createVariable(name, dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
        bio[name].units = 'milimole meter-3'
        bio[name][:,:,:,:] = his.variables[name][t,:,:,:]
        bio[name].time = 'ocean_time'
    return ini


if __name__ == '__main__':

    hisfile = '/Users/teruhisa/Dropbox/Data/ob500_his_0008.nc'
    inifile = '/Users/teruhisa/Dropbox/Data/ob500_his2ini.nc'
    dstart = datetime.datetime(2012, 8, 1, 0, 0, 0)
    make_his2ini(hisfile, inifile, dstart)

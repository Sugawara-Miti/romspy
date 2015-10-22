# -*- coding: utf-8 -*-

import netCDF4
import datetime
import numpy as np
from numpy import dtype


def his2ini(hisfile, inifile, date, redate=None):

    GMT = 'seconds since 1968-05-23 00:00:00 GMT'
    JST = 'seconds since 1968-05-23 09:00:00 GMT'

    daystart = datetime.datetime.strftime(date, '%m%d')
    inifile = inifile.format(daystart)

    his = netCDF4.Dataset(hisfile, 'r')
    ini = netCDF4.Dataset(inifile, 'w', format='NETCDF3_CLASSIC')

    time = his.variables['ocean_time']
    dnum = netCDF4.date2num(date, JST)
    t = np.where(time[:]==dnum)[0][0]

    for name in his.dimensions.keys():
        if name == 'ocean_time':
            ini.createDimension(name, None)
        else:
            ini.createDimension(name, len(his.dimensions[name]))

    time = ini.createVariable('ocean_time', dtype('double').char, ('ocean_time',))
    lon  = ini.createVariable('lon_rho', dtype('float32').char, ('eta_rho', 'xi_rho'))
    lat  = ini.createVariable('lat_rho', dtype('float32').char, ('eta_rho', 'xi_rho'))
    zeta = ini.createVariable('zeta', dtype('float32').char, ('ocean_time', 'eta_rho', 'xi_rho'))
    ubar = ini.createVariable('ubar', dtype('float32').char, ('ocean_time', 'eta_u', 'xi_u'))
    vbar = ini.createVariable('vbar', dtype('float32').char, ('ocean_time', 'eta_v', 'xi_v'))
    u    = ini.createVariable('u', dtype('float32').char, ('ocean_time', 's_rho', 'eta_u', 'xi_u'))
    v    = ini.createVariable('v', dtype('float32').char, ('ocean_time', 's_rho', 'eta_v', 'xi_v'))
    temp = ini.createVariable('temp', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
    salt = ini.createVariable('salt', dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))

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

    if redate is not None:
        time[0] = netCDF4.date2num(redate, JST)
    else:
        time[0] = his.variables['ocean_time'][t]
    lon[:,:]    = his.variables['lon_rho'][:,:]
    lat[:,:]    = his.variables['lat_rho'][:,:]
    zeta[0,:,:] = his.variables['zeta'][t,:,:]
    ubar[0,:,:] = his.variables['ubar'][t,:,:]
    vbar[0,:,:] = his.variables['vbar'][t,:,:]
    u[0,:,:,:]  = his.variables['u'][t,:,:,:]
    v[0,:,:,:]  = his.variables['v'][t,:,:,:]
    temp[0,:,:,:] = his.variables['temp'][t,:,:,:]
    salt[0,:,:,:] = his.variables['salt'][t,:,:,:]

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
        print name
        bio[name] = ini.createVariable(name, dtype('float32').char, ('ocean_time', 's_rho', 'eta_rho', 'xi_rho'))
        bio[name].units = 'milimole meter-3'
        bio[name][0,:,:,:] = his.variables[name][t,:,:,:]
        bio[name].time = 'ocean_time'
    return ini


def initialize(inifile, date, vname, value):
    day = datetime.datetime.strftime(date, '%m%d')
    inifile = inifile.format(day)
    ini = netCDF4.Dataset(inifile, 'r+', format='NETCDF3_CLASSIC')
    var = ini.variables[vname]
    if var.ndim == 3:
        var[0,:,:] = value
    elif var.ndim == 4:
        var[0,:,:,:] = value
    ini.close()


if __name__ == '__main__':

    #hisfile = '/Users/teruhisa/mnt/apps/OB500_fennelP/NL05/ob500_his_0004.nc'
    #inifile = '/Users/teruhisa/Dropbox/Data/ob500_ini_NL05_{}.nc'
    hisfile = 'Z:/roms/Apps/OB500_fennelP/NL10/ob500_rst.nc'
    inifile = 'F:/okada/Dropbox/Data/ob500_rst_NL10_{}.nc'
    import romspy
    print romspy.get_time(hisfile, 'all')
    date = datetime.datetime(2013, 1, 1, 0, 0, 0)
    redate = datetime.datetime(2012, 1, 1, 0, 0, 0)
    #his2ini(hisfile, inifile, date, redate)
    initialize(inifile, redate, 'zeta', 1.5)
    initialize(inifile, redate, 'ubar', 0.0)
    initialize(inifile, redate, 'vbar', 0.0)
    initialize(inifile, redate, 'u', 0.0)
    initialize(inifile, redate, 'v', 0.0)

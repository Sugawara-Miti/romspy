# coding: utf-8

"""
Program to make frcing nc files from observations at osaka

2014-10-21 okada make this file.
"""

import netCDF4
from numpy import dtype
import pandas as pd
import datetime
import numpy as np


def _parse(date, hour):
    """
    parser for time in csvfile
    """
    dt = datetime.datetime.strptime(date, '%Y/%m/%d')
    delta = datetime.timedelta(hours=float(hour))
    return dt + delta


def read_osaka(csvfile):
    """
    csvfile is from dbfile.
    """
    global time_out

    data = pd.read_csv(csvfile, parse_dates=[['date', 'hour']], date_parser=_parse, 
                       a_values='--')
    data = data.interpolate()
    data = data.fillna(method='bfill')
    data['mjd'] = data['date_hour'].apply(
        lambda t: netCDF4.date2num(t, 'days since 1968-05-23 09:00:00 GMT'))
    print data.describe()

    # set data
    nt = len(data)
    time_out = data.mjd.values
    tair_out = np.ndarray(shape=[nt, eta_rho, xi_rho])
    pair_out = np.ndarray(shape=[nt, eta_rho, xi_rho])
    qair_out = np.ndarray(shape=[nt, eta_rho, xi_rho])
    cloud_out = np.ndarray(shape=[nt, eta_rho, xi_rho])
    rain_out = np.ndarray(shape=[nt, eta_rho, xi_rho])
    swrad_out = np.ndarray(shape=[nt, eta_rho, xi_rho])

    for eta in xrange(eta_rho):
        for xi in xrange(xi_rho):
            tair_out[:, eta, xi] = data.temperature          # C
            pair_out[:, eta, xi] = data.air_pressure         # 1 millibar = 1 hPa
            qair_out[:, eta, xi] = data.humidity             # %
            cloud_out[:, eta, xi] = data.cloud/10.0           # 0-10
            rain_out[:, eta, xi] = data.precipitation/3600.0 # 1 kg/m2/s = 3600 mm/h
            swrad_out[:, eta, xi] = data.radiation*10**6/3600 # 1 W/m2 = 3600/(10**6) MJ/m2/h

    return tair_out, pair_out, qair_out, cloud_out, rain_out, swrad_out    


def make_nc(filename, varname, var_out, units):

    nc = netCDF4.Dataset(filename.format(varname), 'w', format='NETCDF3_CLASSIC') 
    now = datetime.datetime.now()
    nc.history = now.strftime('%Y-%m-%d %H:%M:%S')
    nc.author = 'OKADA Teruhisa'
    nc.createDimension('xi_rho', xi_rho)
    nc.createDimension('eta_rho', eta_rho)
    nc.createDimension('time_hourly', None)
    time = nc.createVariable('time_hourly', dtype('double').char, ('time_hourly',) )
    var  = nc.createVariable( varname, dtype('float32').char, ('time_hourly', 'eta_rho', 'xi_rho') )
    time.units = 'days since 1968-05-23 00:00:00 GMT'
    var.units  = units
    time[:] = time_out
    var[:,:,:] = var_out
    var.time = 'time_hourly'
    nc.close()


def make_frc_file():

    global xi_rho, eta_rho
    xi_rho = 117
    eta_rho = 124
    csvfile = '/home/work/okada/OB500/Forcing/jma_osaka/weather_24h/osaka_L.csv'
    frcfile = 'ob500_frc_{}_2012.nc'
    
    tair_out, pair_out, qair_out, cloud_out, rain_out, swrad_out = read_osaka(csvfile)
    make_nc(frcfile, 'Tair',  tair_out,  'Celsius')
    make_nc(frcfile, 'Pair',  pair_out,  'millibar')
    make_nc(frcfile, 'Qair',  qair_out,  'percentage')
    make_nc(frcfile, 'cloud', cloud_out, 'nondimensional')
    make_nc(frcfile, 'rain',  rain_out,  'kilogram meter-2 second-1')
    make_nc(frcfile, 'swrad', swrad_out, 'watt meter-2')

if __name__ == '__main__':

    make_frc_file()

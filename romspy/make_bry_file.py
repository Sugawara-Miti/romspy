# -*- coding: utf-8 -*-

"""
2015/05/01 okada   make this file versio is 2.0
"""

__version__ = 2.0

import datetime

from make import *


bio_units = {'others':'millimole meter-3',
             'chrolophyll':'milligram meter-3',
             'alkalinity':'milliequivalens meter-3'}


def make_bry_file(dims, dates, zetafiles, wqfiles, biofiles=False, 
                  ncfile='test_bry.nc'):

    """
    use bio_fennel_linear()
    """

    # read
    zeta_out = bry_zeta_dat(dims, zetafiles)
    temp_out = bry_wq_csv(dims, 'temp', wqfiles, dates)
    salt_out = bry_wq_csv(dims, 'salt', wqfiles, dates)
    #bio_out, bio_index = bry_bio_fennel(dims, biofiles)
    bio_out, bio_index = bry_bio_fennel_linear(dims, biofiles)   
    time_out = bry_time_bio(dates, bio_index)

    # write
    nc = netCDF4.Dataset(ncfile, 'w', format='NETCDF3_CLASSIC') 
    now = datetime.datetime.now()
    nc.history = now.strftime('%Y-%m-%d %H:%M:%S')
    nc.author = 'OKADA Teruhisa'
    nc.createDimension('xi_rho',  dims['xi'])
    nc.createDimension('eta_rho', dims['eta'])
    nc.createDimension('xi_u',    dims['xi']-1)
    nc.createDimension('eta_u',   dims['eta'])
    nc.createDimension('xi_v',    dims['xi'])
    nc.createDimension('eta_v',   dims['eta']-1)
    nc.createDimension('s_rho',   dims['s'])

    # write time
    bry_write_time(nc, time_out)

    # write variables
    bry_write_2d(nc, 'zeta', zeta_out, 'time_hourly',   'rho', 'meter')  
    bry_write_2d(nc, 'ubar', {'w':0, 's':0}, 'time_annually', 'u', 'meter second-1')
    bry_write_2d(nc, 'vbar', {'w':0, 's':0}, 'time_annually', 'v', 'meter second-1')
    bry_write_3d(nc, 'u',    {'w':0, 's':0}, 'time_annually', 'u', 'meter second-1')
    bry_write_3d(nc, 'v',    {'w':0, 's':0}, 'time_annually', 'v', 'meter second-1')
    bry_write_3d(nc, 'temp', temp_out, 'time_daily', 'rho', 'Celsius')
    bry_write_3d(nc, 'salt', salt_out, 'time_daily', 'rho', 'PSU')

    for name in bio_out.keys():
        units = bio_units[name] if name in bio_units else bio_units['others']
        bry_write_3d(nc, name, bio_out[name], 'time_biology', 'rho', units)

    nc.close()


if __name__ == '__main__':

    dims = {'xi':117, 'eta':124, 's':20}

    dates = ['2012-01-01', '2013-01-01']

    zetafiles = ['test/data/zeta_hour/2012_Awazu/zeta.dat',
                 'test/data/zeta_hour/2012_Ei/zeta.dat',
                 'test/data/zeta_hour/2012_Kainan/zeta.dat',
                 'test/data/zeta_hour/2012_Takasago/zeta.dat']

    wqfiles = {'w':'test/data/wq_akashi_2012.csv',
               's':'test/data/wq_sumoto_2012.csv'}

    biofiles = {'w':'test/data/fennel_w_linear.csv',
                's':'test/data/fennel_s_linear.csv'}

    ncfile = 'ob500_bry_fennel_2012_linear.nc'

    make_bry_file(dims, dates, zetafiles, wqfiles, biofiles, ncfile)

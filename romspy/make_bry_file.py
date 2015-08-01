# -*- coding: utf-8 -*-

"""
2015/05/01 okada   make this file versio is 2.0
"""

import datetime
import netCDF4

from make import *

__version__ = 3.0
bio_units = {'others':'millimole meter-3',
             'chrolophyll':'milligram meter-3',
             'alkalinity':'milliequivalens meter-3'}


def make_bry_file(ncfile, dims, dates, zetafiles, wqfiles, biofiles=None, bio=None):

    """
    use bio_fennel_linear()
    """

    # read
    zeta_out = bry_zeta_dat(dims, zetafiles)
    temp_out = bry_wq_csv(dims, 'temp', wqfiles, dates)
    salt_out = bry_wq_csv(dims, 'salt', wqfiles, dates)
    if biofiles is not None:
        # bio_out, bio_index = bry_bio_fennel(dims, biofiles)
        bio_out, bio_index = bry_bio_fennel_linear(dims, biofiles)
        time_out = bry_time(dates, bio_index)
    elif bio == 'fennelP':
        bio_out, bio_dtime = bry_bio_fennelP(dims) 
        time_out = bry_time(dates, bio_dtime)
    else:
        time_out = bry_time(dates)

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

    if (biofiles is not None) or (bio is not None):
        for name in bio_out['w'].keys():
            units = bio_units[name] if name in bio_units else bio_units['others']
            bry_write_3d(nc, name, {d:bio_out[d][name] for d in ['w','s']}, 'time_biology', 'rho', units)

    nc.close()


if __name__ == '__main__':

    ncfile = '/Users/teruhisa/Dropbox/Data/ob500_bry_2012_fennelP-1.nc'

    dims = {'xi':117, 'eta':124, 's':20}
    dates = ['2012-01-01', '2013-01-01']
    zetafiles = ['/Users/teruhisa/Dropbox/Data/zeta_hour/2012_Awazu/zeta.dat',
                 '/Users/teruhisa/Dropbox/Data/zeta_hour/2012_Ei/zeta.dat',
                 '/Users/teruhisa/Dropbox/Data/zeta_hour/2012_Kainan/zeta.dat',
                 '/Users/teruhisa/Dropbox/Data/zeta_hour/2012_Takasago/zeta.dat']
    wqfiles = {'w':'/Users/teruhisa/Dropbox/Data/bry_wq_akashi_2012.csv',
               's':'/Users/teruhisa/Dropbox/Data/bry_wq_sumoto_2012.csv'}
    #biofiles = {'w':'/Users/teruhisa/Dropbox/Data/fennel_w_linear.csv',
    #            's':'/Users/teruhisa/Dropbox/Data/fennel_s_linear.csv'}

    make_bry_file(ncfile, dims, dates, zetafiles, wqfiles, bio='fennelP')

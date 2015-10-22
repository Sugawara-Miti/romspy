# coding: utf-8
# (c) 2015 Teruhisa Okada
# 2015/05/01 2.0
#            3.0
# 2015/10/14 3.1
# 2015/10/14 3.2

import datetime
import netCDF4

from boundary import *

__version__ = 3.2
bio_units = {'others':'millimole meter-3',
             'chlorophyll':'milligram meter-3',
             'alkalinity':'milliequivalens meter-3'}


def make_bry_file(ncfile, dims, dates, zetafiles, tempfiles, biofiles=None, biofiles2=None):

    # read
    zeta_out = bry_zeta_dat(dims, zetafiles)
    temp_out, time_temp = bry_var(dims, tempfiles, dates, 'D')  # ver3.1
    #temp_out = bry_wq_csv(dims, 'temp', wqfiles, dates)
    #salt_out = bry_wq_csv(dims, 'salt', wqfiles, dates)
    if biofiles is not None:
        bio_out, time_biology = bry_var(dims, biofiles, dates) 
    if biofiles2 is not None:
        bio_out2, time_biology2 = bry_var(dims, biofiles2, dates)

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
    time = bry_time(dates)
    bry_write_time(nc, 'time_annually', time['annually'])
    #bry_write_time(nc, 'time_daily', time['daily'])
    bry_write_time(nc, 'time_hourly', time['hourly'])
    bry_write_time(nc, 'time_temp', time_temp)
    bry_write_time(nc, 'time_biology', time_biology)
    #bry_write_time(nc, 'time_biology2', time_biology2)

    # write variables
    bry_write_2d(nc, 'zeta', zeta_out, 'time_hourly', 'rho', 'meter')  
    bry_write_2d(nc, 'ubar', {'w':0, 's':0}, 'time_annually', 'u', 'meter second-1')
    bry_write_2d(nc, 'vbar', {'w':0, 's':0}, 'time_annually', 'v', 'meter second-1')
    bry_write_3d(nc, 'u',    {'w':0, 's':0}, 'time_annually', 'u', 'meter second-1')
    bry_write_3d(nc, 'v',    {'w':0, 's':0}, 'time_annually', 'v', 'meter second-1')
    bry_write_3d(nc, 'temp', temp_out, 'time_temp', 'rho', 'Celsius')
    bry_write_3d(nc, 'salt', {'w':32, 's':32.5}, 'time_annually', 'rho', 'PSU')

    if biofiles is not None:
        for name in bio_out.keys():
            units = bio_units[name] if name in bio_units else bio_units['others']
            bry_write_3d(nc, name, bio_out[name], 'time_biology', 'rho', units)
    if biofiles2 is not None:
        for name in bio_out2.keys():
            units = bio_units[name] if name in bio_units else bio_units['others']
            bry_write_3d(nc, name, bio_out2[name], 'time_biology2', 'rho', units)

    nc.close()


if __name__ == '__main__':

    ncfile = 'F:/okada/Dropbox/Data/ob500_bry_2012_fennelP-5.nc'
    #ncfile = 'V:/ROMS/boundary/ob500_bry_2012_fennelP-5.nc'
    dims = {'xi':117, 'eta':124, 's':20}
    dates = ['2012-01-01', '2013-01-01']
    zeta = ['V:/ROMS/boundary/zeta_hour/2012_Awazu/zeta.dat',
            'V:/ROMS/boundary/zeta_hour/2012_Ei/zeta.dat',
            'V:/ROMS/boundary/zeta_hour/2012_Kainan/zeta.dat',
            'V:/ROMS/boundary/zeta_hour/2012_Takasago/zeta.dat']
    temp = {}
    temp['south_bot'] = 'V:/ROMS/boundary/temp_south_bot_A11_2012.csv'
    temp['south_sur'] = 'V:/ROMS/boundary/temp_south_sur_A11_2012.csv'
    temp['west_bot'] = 'V:/ROMS/boundary/temp_west_bot_akashi_2012.csv'
    temp['west_sur'] = 'V:/ROMS/boundary/temp_west_sur_akashi_2012.csv'
    bio = {}
    bio['west'] = 'V:/ROMS/boundary/bio_west_seto_2001-2013_15D.csv'
    bio['south'] = 'V:/ROMS/boundary/bio_south_seto_2001-2013_15D.csv'
    bio['others'] = 'V:/ROMS/boundary/bio_others.csv'
    #oxygen = {}
    #oxygen['west'] = 'V:/ROMS/boundary/oxygen_west.csv'
    #oxygen['south'] = 'V:/ROMS/boundary/oxygen_south.csv'

    make_bry_file(ncfile, dims, dates, zeta, temp, bio)

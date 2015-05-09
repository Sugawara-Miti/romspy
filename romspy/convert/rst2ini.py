# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import netCDF4
import datetime
import shutil
import os

def rst2ini(rstfile, inifile, dstart):

    print rstfile
    print inifile
    print dstart

    try: 
        cmd = 'copy {} {}'.format(rstfile, inifile)
        os.system(cmd)
    except:
        shutil.copyfile(rstfile, inifile)

    nc = netCDF4.Dataset(inifile, 'r+')

    print nc.variables['ocean_time'][:]

    # <codecell>

    nc.variables['zeta'][:,:,:] = 0.0
    nc.variables['ubar'][:,:,:] = 0.0
    nc.variables['vbar'][:,:,:] = 0.0
    nc.variables['u'][:,:,:,:]  = 0.0
    nc.variables['v'][:,:,:,:]  = 0.0

    # <codecell>

    units  = nc.variables['ocean_time'].units
    dstart = dstart - datetime.timedelta(hours=9)
    start  = netCDF4.date2num(dstart, units)
    
    nc.variables['ocean_time'][:] = start

    print nc.variables['ocean_time'][:]

    nc.close()

# <codecell>

if __name__ == '__main__':

    rstfile = '../roms2-4/ob500_rst.nc'

    inifile = 'ob500_ini_roms2-4.nc'

    dstart = datetime.datetime(2012, 1, 1, 0, 0, 0)
    
    rst2ini(rstfile, inifile, dstart)

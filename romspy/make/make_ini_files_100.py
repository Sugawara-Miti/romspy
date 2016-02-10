# coding: utf-8
# (c) 2015-11-21 Teruhisa Okada

import datetime
import shutil
import random
import netCDF4
import numpy as np
import romspy

hisfile = '/home/okada/ism-i/apps/OB500P/case21/NL1_3/ob500_rst.nc'
inifile = '/home/okada/Data/ini_100/ob500_ini_case21_NL1_3_0101_%d.nc'

date = datetime.datetime(2013, 1, 1, 0, 0, 0)
redate = datetime.datetime(2012, 1, 1, 0, 0, 0)

N = 100


def _add_random(inifile):
    ini = netCDF4.Dataset(inifile, 'r+', format='NETCDF3_CLASSIC')
    mask = np.where(ini.variables['mask_rho'][:,:] == 1)
    for vname in ini.variables.keys():
        if vname in ['u', 'v']:
            continue
        var = ini.variables[vname]
        if var.ndim == 4:
            vmean = np.mean([var[0,k,:,:][mask] for k in range(20)])
            delta = vmean * random.uniform(-0.1, 0.1)
            var[0,:,:,:] += delta
    ini.close()

romspy.his2ini(hisfile, inifile, date, redate)

for i in range(N):
    inifile_i = inifile % i
    print inifile, '=>', inifile_i
    shutil.copyfile(inifile, inifile_i)
    _add_random(inifile_i)

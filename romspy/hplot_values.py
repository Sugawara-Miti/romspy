# -*- coding: utf-8 -*-
"""
Title: plot surface current
Author: okada
Created on Tue Dec 17 18:05:24 2013

hplot_4dvar: change to read 4dvar fwd file
"""

import netCDF4
import matplotlib.pyplot as plt
#import matplotlib.cm as cm
import romspy
import numpy as np


def xy2lonlat(x, y, grdfile):

    grid = netCDF4.Dataset(grdfile, 'r')

    lon = grid.variables['lon_rho'][0,:]
    lat = grid.variables['lat_rho'][:,0]

    return lon[x], lat[y]


def hplot_values(obsfile, varid, plotdate, vmin=None, vmax=None, grdfile=None, cff=1.0):
    print obsfile, varid, plotdate, vmin, vmax, grdfile
    obs = netCDF4.Dataset(obsfile, 'r')
    obs_time = obs.variables['obs_time'][:]
    plottime = netCDF4.date2num(plotdate, romspy.JST_days)
    index = np.where(obs_time==plottime)
    try:
        obs_lon = obs.variables['obs_lon'][index]
        obs_lat = obs.variables['obs_lat'][index]
    except:
        obs_Xgrid = obs.variables['obs_Xgrid'][index]
        obs_Ygrid = obs.variables['obs_Ygrid'][index]
    obs_depth = obs.variables['obs_depth'][index]
    obs_type = obs.variables['obs_type'][index]
    obs_value = obs.variables['obs_value'][index]
    obs.close()
    try:
        obs_zip = zip(obs_time, obs_lon, obs_lat, obs_depth, obs_type, obs_value)
    except:
        obs_zip = zip(obs_time, obs_Xgrid, obs_Ygrid, obs_depth, obs_type, obs_value)
    flag = 0
    check = {}
    ax = plt.gca()
    for i, (t, x, y, z, type, v) in enumerate(obs_zip):
        try:
            lon, lat = x, y
        except:
            lon, lat = xy2lonlat(x, y, grdfile)
        if type == varid:
            if not lon in check.keys():
                print i, t, x, y, z, type, v
                check[lon] = z
                sc = ax.scatter(lon, lat, c=v*cff, vmin=vmin, vmax=vmax, s=200)
                #plt.text(lon-0.01, lat-0.02, str(round(v,1)))
            elif z < check[lon]:
                print i, t, x, y, z, type, v
                check[lon] = z
                sc = ax.scatter(lon, lat, c=v*cff, vmin=vmin, vmax=vmax, s=200)

    return sc


if __name__ == '__main__':
    import datetime
    romspy.cmap('jet')
    obsfile = '/home/okada/Data/ob500_obs_2012_mp-2.nc'
    varid = 15
    plotdate = datetime.datetime(2012,8,3,0)
    vmin = 0
    vmax = 10
    cff = romspy.mol2g_O2
    romspy.basemap()
    sc = hplot_values(obsfile, varid, plotdate, vmin=vmin, vmax=vmax, cff=cff)
    plt.colorbar(sc)
    plt.show()

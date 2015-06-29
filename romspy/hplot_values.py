# -*- coding: utf-8 -*-
"""
Title: plot surface current
Author: okada
Created on Tue Dec 17 18:05:24 2013

hplot_4dvar: change to read 4dvar fwd file
"""

# import

import netCDF4
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# main ----------------------------------------------------------

def xy2lonlat(x, y, grdfile):

    grid = netCDF4.Dataset(grdfile, 'r')

    lon = grid.variables['lon_rho'][0,:]
    lat = grid.variables['lat_rho'][:,0]

    return lon[x], lat[y]

def hplot_values(obsfile, varid, plotdate, vmin=None, vmax=None, grdfile=None):

    obs = netCDF4.Dataset(obsfile, 'r')
    obs_time = obs.variables['obs_time'][:]
    try:
        obs_lon = obs.variables['obs_lon'][:]
        obs_lat = obs.variables['obs_lat'][:]
    except:
        obs_Xgrid = obs.variables['obs_Xgrid'][:]
        obs_Ygrid = obs.variables['obs_Ygrid'][:]
    obs_depth = obs.variables['obs_depth'][:]
    obs_type = obs.variables['obs_type'][:]
    obs_value = obs.variables['obs_value'][:]
    obs.close()
    
    time_units = "day since 2012-06-01 00:00:00"
    obs_time = netCDF4.num2date(obs_time, time_units)

    try:
        obs_zip = zip(obs_time, obs_lon, obs_lat, obs_depth, obs_type, obs_value)
    except:
        obs_zip = zip(obs_time, obs_Xgrid, obs_Ygrid, obs_depth, obs_type, obs_value)
    flag = 0
    check = []

    ax = plt.gca()
    
    for i, (t, x, y, z, type, v) in enumerate(obs_zip):
        if t == plotdate:
            flag = 1
            try:
                lon, lat = obs_lon, obs_lat
            except:
                lon, lat = xy2lonlat(x, y, grdfile)
            
            if type == varid and z >= -1.0:
                
                if not [lon, lat] in check:
                    check.append([lon, lat])

                    ax.scatter(lon, lat, c=v*2.18, cmap=cm.jet, 
                               vmin=vmin, vmax=vmax, s=200)
                    #plt.text(lon-0.01, lat-0.02, str(round(v,1)))

        elif flag == 1:
            break


# -*- coding: utf-8 -*-

"""
2015/05/01 okada make this file.
2015/05/10 okada enable hview to handle grid nc file,
                 and add plot_obs_positions.
"""

import netCDF4
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
import pandas as pd

from basemap import basemap

def hview(ncfile, figfile=None, vname=None, t=-1, k=None, vmax=None, vmin=None,
          interval=1, fmt='%i', cff=1.0, cblabel=None, obsfile=None,
          mapfile=None):

    # read
    nc = netCDF4.Dataset(ncfile, 'r')
    x_rho = nc.variables['lon_rho'][0,:]-0.00449/2
    y_rho = nc.variables['lat_rho'][:,0]-0.00546/2
    ndim = len(nc.variables[vname].shape)
    if ndim is 2:
        var2d = nc.variables[vname][:,:] * cff
    else:
        ocean_time = nc.variables['ocean_time'][t]
        tunits = nc.variables['ocean_time'].units
        if ndim is 4:
            var2d = nc.variables[vname][t,k-1,:,:] * cff
        if ndim is 3:
            var2d = nc.variables[vname][t,:,:] * cff
    nc.close()

    # pcolor
    plt.figure(figsize=(6,5))
    X, Y = np.meshgrid(x_rho, y_rho)
    if vmax is not None:
        PC = plt.pcolor(X, Y, var2d, vmax=vmax, vmin=vmin)
    else:
        PC = plt.pcolor(X, Y, var2d)
    cbar = plt.colorbar(PC)
    cbar.ax.set_ylabel(cblabel)

    # contour
    if vmax is not None:
        interval = np.arange(vmin, vmax, interval)
    else:
        interval = np.arange(np.min(var2d), np.max(var2d), interval)
    if vname == 'h':
        matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    CF = plt.contour(X+0.00449, Y+0.00546, var2d, interval, colors='k', ls='-')
    CF.clabel(fontsize=9, fmt=fmt, c='k')

    # basemap
    if mapfile is not None:
        basemap(mapfile)
    else:
        basemap()

    # finalize
    if ndim is 2:
        title = 'Model domein & bathymetry'
    else:
        dtime = netCDF4.num2date(ocean_time, units=tunits)
        title = datetime.datetime.strftime(dtime,'%Y-%m-%d %H:%M:%S')
    plt.title(title)
    if figfile is not None:
        plt.savefig(figfile, bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    
    from hplot_stations import hplot_stations
    from hplot_values import hplot_values

    test = 2
    
    if test == 0:
        hview('../example/OB500/nc/ob500_avg.nc',
              '../example/OB500/ob500_avg_temp_t0_k20.png',
              vname='temp', t=0, k=20, cblabel='Temperature[C]')
        
    if test == 1:
        hview('../example/OB500/nc/ob500_grd-v5.nc',
              vname='h', cblabel='Depth[m]',
              vmax=0, vmin=-120, interval=20, cff=-1)
        hplot_stations('../../OB500/Data/ob500_obs_tsdc.nc')
        plt.savefig('../example/OB500/ob500_grd-v5.png', bbox_inches='tight')
        
    if test == 2:
        hview('../example/OB500/nc/ob500_avg.nc',
              vname='temp', t=0, k=20, cblabel='Temperature[C]')
        
        hplot_values('../../OB500/Data/ob500_obs_tsdc.nc',
                     6, datetime.datetime(2012,8,24,6))
        
        plt.savefig('../example/OB500/ob500_avg_temp_t0_k20_values.png', bbox_inches='tight')

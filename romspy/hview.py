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

def hview(ncfile, pngfile, vname, t=-1, k=None, vmax=None, vmin=None,
          interval=1, fmt='%i', cff=1.0, cblabel=None, obsfile=None):

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
    CF = plt.contour(X, Y, var2d, interval, colors='k', ls='-')
    CF.clabel(fontsize=9, fmt=fmt, c='k')

    # basemap
    basemap()

    # observations
    if obsfile is not None:
        plot_obs_positions(obsfile)

    # finalize
    if ndim is 2:
        title = 'Model domein & bathymetry'
    else:
        dtime = netCDF4.num2date(ocean_time, units=tunits)
        title = datetime.datetime.strftime(dtime,'%Y-%m-%d %H:%M:%S')
    plt.title(title)
    plt.savefig(pngfile, bbox_inches='tight')
    plt.close()

def plot_obs_positions(obsfile):

    """
    You can use csv and nc file.
    """

    if obsfile[-3:] == 'csv':
        df = pd.read_csv(obsfile)
        print df
    elif obsfile[-2:] == 'nc':
        nc = netCDF4.Dataset(obsfile, 'r')
        obs = {}
        obs['lon'] = nc.variables['obs_lon'][:]
        obs['lat'] = nc.variables['obs_lat'][:]
        obs['station'] = nc.variables['obs_station'][:]
        df = pd.DataFrame(obs)
        df = df.drop_duplicates()
        print df
    else:
        print obsfile[-3:]
        pass
    
    plt.scatter(df.lon, df.lat, s=40, c='w', marker='o', lw=2)

    names = ['Sta.{}'.format(s) for s in df.station.values]
    bbox_props = dict(boxstyle="square", fc="w")

    """
    for x, y, name in zip(obs_lon, obs_lat, names):
        if name == 'Sta.4' or name == 'Sta.5' or name == 'Sta.12':
            plt.text(x-0.01, y-0.01, name, ha="right", va="top", bbox=bbox_props, fontsize=10)
    """

if __name__ == '__main__':

    test = 1
    
    if test == 0:
        hview('../example/OB500/nc/ob500_avg.nc',
              '../example/OB500/ob500_avg_temp_t0_k20.png',
              'temp', t=0, k=20, cblabel='Temperature[C]')
    if test == 1:
        hview('../example/OB500/nc/ob500_grd-v5.nc',
              '../example/OB500/ob500_grd-v5.png',
              'h', cblabel='Depth[m]', vmax=0, vmin=-120, interval=20, cff=-1,
              obsfile='/home/work/okada/OB500/Data/ob500_obs_tsdc.nc')
              #obsfile='/home/work/okada/OB500/OBS/st/obs_stations.csv')

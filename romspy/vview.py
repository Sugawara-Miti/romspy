# -*- coding: utf-8 -*-

"""
2015/05/27 okada make this file.
"""

import netCDF4
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
import pandas as pd

def vview(linefile, ncfile, vname, t=-1, k=None, vmax=None, vmin=None,
          interval=1, fmt='%i', cff=1.0, cblabel=None, obsfile=None):

    # resd line
    line = pd.read_csv(linefile)

    # read
    nc = netCDF4.Dataset(ncfile, 'r')
    x_rho = nc.variables['lon_rho'][0,:]-0.00449/2
    y_rho = nc.variables['lat_rho'][:,0]-0.00546/2
    ndim = len(nc.variables[vname].shape)
    ocean_time = nc.variables['ocean_time'][t]
    tunits = nc.variables['ocean_time'].units
    var2d = np.ndarray(shape=[20, len(line)])
    for i in range(len(line)):
        var2d[:,i] = nc.variables[vname][t, :, line.x_rho[i], line.y_rho[i] * cff]
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

    test = 0

    if test == 0:
        vview('/home/okada/Dropbox/Data/line.csv',
              '/home/okada/Dropbox/Data/ob500_rst_NL08_0101.nc',
              'chlorophyll')

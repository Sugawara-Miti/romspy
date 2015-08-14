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

from basemap import basemap


def hview(ncfile, vname, time=None, k=None, interval=None, fmt='%i', cff=1.0, 
          cblabel=None, mapfile=None, cmap='jet', figfile=None, grdfile=None):

    JST = 'seconds since 1968-05-23 09:00:00 GMT'

    # read
    nc = netCDF4.Dataset(ncfile, 'r')
    print vname, ncfile

    if grdfile is not None:
        grd = netCDF4.Dataset(grdfile, 'r')
        x_rho = grd.variables['lon_rho'][0,:]-0.00449/2
        y_rho = grd.variables['lat_rho'][:,0]-0.00546/2
        grd.close()
    else:
        x_rho = nc.variables['lon_rho'][0,:]-0.00449/2
        y_rho = nc.variables['lat_rho'][:,0]-0.00546/2

    if time is not None:
        t = netCDF4.date2num(time, JST)
        ocean_time = nc.variables['ocean_time'][:]
        # print netCDF4.num2date(ocean_time[0], JST), "-", netCDF4.num2date(ocean_time[-1], JST)
        t = np.where(ocean_time==t)[0][0]
    else:
        t = 0

    var = nc.variables[vname]
    if var.ndim == 4:
        var2d = var[t,k-1,:,:] * cff
    elif var.ndim == 3:
        var2d = var[t,:,:] * cff
    else:
        var2d = var[:,:] * cff
    nc.close()

    # pcolor
    ax = plt.gca()
    X, Y = np.meshgrid(x_rho, y_rho)
    if interval is not None:
        PC = ax.pcolor(X, Y, var2d, cmap=cmap, vmin=interval[0], vmax=interval[-1])
    else:
        PC = ax.pcolor(X, Y, var2d, cmap=cmap)
    cbar = plt.colorbar(PC)
    if cblabel is not None:
        cbar.ax.set_ylabel(cblabel)
    else:
        cbar.ax.set_ylabel(vname)

    # contour
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    if interval is not None:
        CF = plt.contour(X+0.00449, Y+0.00546, var2d, interval, colors='k', ls='-')
    else:
        CF = plt.contour(X+0.00449, Y+0.00546, var2d, colors='k', ls='-')
    CF.clabel(fontsize=9, fmt=fmt, c='k')

    # basemap
    if mapfile is not None:
        basemap(mapfile)
    else:
        basemap()

    # finalize
    if vname == 'h':
        plt.title('Model domein & bathymetry')
    else:
        plt.title(datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S'))

    if figfile is not None:
        plt.savefig(figfile, bbox_inches='tight')
        plt.close()
    else:
        return ax


def ini_diff(ncfile, vname, k=None, interval=None, fmt='%i', cff=1.0, 
             cblabel=None, mapfile=None, cmap='jet', figfile=None, grdfile=None):

    JST = 'seconds since 1968-05-23 09:00:00 GMT'

    # read
    nc = netCDF4.Dataset(ncfile, 'r')
    print ncfile

    if grdfile is not None:
        grd = netCDF4.Dataset(grdfile, 'r')
        x_rho = grd.variables['lon_rho'][0,:]-0.00449/2
        y_rho = grd.variables['lat_rho'][:,0]-0.00546/2
        grd.close()
    else:
        x_rho = nc.variables['lon_rho'][0,:]-0.00449/2
        y_rho = nc.variables['lat_rho'][:,0]-0.00546/2

    ocean_time = nc.variables['ocean_time'][0]
    time = netCDF4.num2date(ocean_time, JST)
    var = nc.variables[vname]
    if var.ndim == 4:
        var = var[:,k-1,:,:] * cff
    else:
        var = var[:,:,:] * cff
    nc.close()
    var2d = var[1,:,:] - var[0,:,:]

    # pcolor
    ax = plt.gca()
    X, Y = np.meshgrid(x_rho, y_rho)
    if interval is not None:
        PC = ax.pcolor(X, Y, var2d, cmap=cmap, vmin=interval[0], vmax=interval[-1])
    else:
        PC = ax.pcolor(X, Y, var2d, cmap=cmap)
    cbar = plt.colorbar(PC)
    if cblabel is not None:
        cbar.ax.set_ylabel(cblabel)
    else:
        cbar.ax.set_ylabel(vname)

    # contour
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    if interval is not None:
        CF = plt.contour(X+0.00449, Y+0.00546, var2d, interval, colors='k', ls='-')
    else:
        CF = plt.contour(X+0.00449, Y+0.00546, var2d, colors='k', ls='-')
    CF.clabel(fontsize=9, fmt=fmt, c='k')

    # basemap
    if mapfile is not None:
        basemap(mapfile)
    else:
        basemap()

    # finalize
    plt.title(datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S'))

    if figfile is not None:
        plt.savefig(figfile, bbox_inches='tight')
        plt.close()
    else:
        return ax


def _test4():
    ncfile = '/home/okada/roms/Apps/OB500A/I4DVAR01/ob500a_ini.nc'
    mapfile = '/home/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    ini_diff(ncfile, 'temp', 20, mapfile=mapfile, figfile="hview_test4.png", interval=np.arange(-1.0,1.1,2))


if __name__ == '__main__':
    _test4()

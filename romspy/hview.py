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
        if k is not None:
            var2d = nc.variables[vname][t,k-1,:,:] * cff
        else:
            var2d = nc.variables[vname][t,:,:] * cff
    else:
        var2d = nc.variables[vname][:,:] * cff
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
    if k is not None:
        var2d = nc.variables[vname][:,k-1,:,:] * cff
    else:
        var2d = nc.variables[vname][:,:,:] * cff
    nc.close()
    var2d = var2d[1,:,:] - var2d[0,:,:]

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


def _test1():
    import datetime as dt
    time = dt.datetime(2012, 3, 5, 12)
    ncfile = '/Users/teruhisa/Dropbox/Data/OB500_fennelP/NL02/ob500_dia_0003.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview(ncfile, 'SOD', time, interval=np.arange(-30,1,5), mapfile=mapfile)
    plt.savefig("hview_test.png")


def _test2():
    import datetime as dt
    time = dt.datetime(2012, 8, 5, 0)
    ncfile = '/Users/teruhisa/mnt/apps/OB500_fennelP/I4DVAR/ob500_ini.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview(ncfile, 'temp', time, 20, mapfile=mapfile, figfile="hview_test2.png")


def _test3():
    ncfile = '/Users/teruhisa/mnt/apps/OB500_fennelP/I4DVAR01/ob500_ini.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    ini_diff(ncfile, 'temp', 20, interval=np.arange(-1.0,1.1,1), mapfile=mapfile, figfile="hview_test3.png")


def _test4():
    ncfile = '/home/okada/roms/Apps/OB500A/I4DVAR01/ob500a_ini.nc'
    mapfile = '/home/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    ini_diff(ncfile, 'zeta', interval=np.arange(-1.0,1.1,2), mapfile=mapfile, figfile="hview_test4.png")


if __name__ == '__main__':

    _test4()

    """
    from hplot_stations import hplot_stations
    from hplot_values import hplot_values

    hview('../example/OB500/nc/ob500_avg.nc',
          '../example/OB500/ob500_avg_temp_t0_k20.png',
          vname='temp', t=0, k=20, cblabel='Temperature[C]')

    hview('../example/OB500/nc/ob500_grd-v5.nc',
          vname='h', cblabel='Depth[m]',
          vmax=0, vmin=-120, interval=20, cff=-1)
    hplot_stations('../../OB500/Data/ob500_obs_tsdc.nc')
    plt.savefig('../example/OB500/ob500_grd-v5.png', bbox_inches='tight')

    hview('../example/OB500/nc/ob500_avg.nc',
          vname='temp', t=0, k=20, cblabel='Temperature[C]')
    hplot_values('../../OB500/Data/ob500_obs_tsdc.nc',
                 6, datetime.datetime(2012,8,24,6))
    plt.savefig('../example/OB500/ob500_avg_temp_t0_k20_values.png', 
                bbox_inches='tight')
    """

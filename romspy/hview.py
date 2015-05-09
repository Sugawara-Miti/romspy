# -*- coding: utf-8 -*-

"""
2015/05/01 okada make this file.
"""

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import datetime

from basemap import basemap

def hview(ncfile, pngfile, vname, t=-1, k=None, vmax=None, vmin=None,
          interval=1, fmt='%i', cff=1.0, cblabel=None):

    # read
    nc = netCDF4.Dataset(ncfile, 'r')
    x_rho = nc.variables['lon_rho'][0,:]-0.00449/2
    y_rho = nc.variables['lat_rho'][:,0]-0.00546/2
    ocean_time = nc.variables['ocean_time'][t]
    tunits = nc.variables['ocean_time'].units
    ndim = len(nc.variables[vname].shape)
    if ndim is 4:
        var2d = nc.variables[vname][t,k-1,:,:] * cff
    if ndim is 3:
        var2d = nc.variables[vname][t,:,:] * cff
    nc.close()

    # pcolor
    plt.figure(figsize=(6,5))
    X, Y = np.meshgrid(x_rho, y_rho)
    PC = plt.pcolor(X, Y, var2d)
    cbar = plt.colorbar(PC)
    cbar.ax.set_ylabel(cblabel)

    # contour
    if vmax is not None:
        interval = np.arange(vmin,vmax,interval)
    else:
        interval = np.arange(np.min(var2d), np.max(var2d), interval)
    CF = plt.contour(X, Y, var2d, interval, colors='k', ls='-')
    CF.clabel(fontsize=9, fmt=fmt, c='k')

    # basemap
    basemap()

    # finalize
    dtime = netCDF4.num2date(ocean_time, units=tunits)
    title = datetime.datetime.strftime(dtime,'%Y-%m-%d %H:%M:%S')
    plt.title(title)
    plt.savefig(pngfile, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':

    ncfile = 'test/nc/ob500_rst.nc'
    pngfile = 'ob500_rst_temp.png'

    hview(ncfile, pngfile, 'temp', k=1, cblabel='Temperature[C]')

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

    # read nc
    nc = netCDF4.Dataset(ncfile, 'r')
    x_rho = nc.variables['lon_rho'][0,:]-0.00449/2
    y_rho = nc.variables['lat_rho'][:,0]-0.00546/2
    var2d = nc.variables[vname][:,:] * cff
    nc.close()

    # pcolor
    plt.figure(figsize=(6,5))
    X, Y = np.meshgrid(x_rho, y_rho)
    PC = plt.pcolor(X, Y, var2d, vmax=0, vmin=-120)
    cbar = plt.colorbar(PC)
    cbar.ax.set_ylabel(cblabel)

    # contour
    interval = np.arange(-120, 0, interval)
    CF = plt.contour(X, Y, var2d, interval, colors='k', ls='-')
    CF.clabel(fontsize=9, fmt=fmt, c='k')

    # basemap
    basemap()

    # other
    plt.title('Model domein & bathymetry')
    plt.savefig(pngfile.format(vname, k), bbox_inches='tight')
    plt.close()

if __name__ == '__main__':

    ncfile = 'test/nc/ob500_grd-v5.nc'
    pngfile = 'ob500_grd.png'

    hview(ncfile, pngfile, 'h', cff=-1, interval=20, cblabel='Depth[m]')

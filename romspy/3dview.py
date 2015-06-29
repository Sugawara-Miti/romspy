#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
2014/08/28 okada created this file.
2015/05/01 okada remade it.
"""

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import *
import numpy as np
import netCDF4

def main(ncfile, vname, k=0, t=0, zlabel=None):

    nc = netCDF4.Dataset(ncfile, 'r')
    x = nc.variables['lon_rho'][0,:]
    y = nc.variables['lat_rho'][:,0]
    if vname == 'h':
        z = -nc.variables['h'][:,:]
    elif len(nc.variables[vname].shape) == 4:
        z = nc.variables[vname][t,k-1,:,:]
        z = z.filled(z.min())
    else:
        z = nc.variables[vname][t,:,:]
        z = z.filled(z.min())
    zunit = nc.variables[vname].units
    nc.close()

    xm, ym = np.meshgrid(x, y)

    fig = plt.figure(facecolor='w')#, figsize=(20, 10))

    ax = fig.add_subplot(111, projection='3d', axisbg='w')

    surf = ax.plot_surface(xm, ym, z, rstride=1, cstride=1, linewidth=0.3,
                           cmap=cm.jet,
                           antialiased=True)

    fig.colorbar(surf, shrink=0.7)
    #fig.colorbar(surf, orientation='horizontal', shrink=0.5)
    #, shrink=0.5, aspect=5)

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    if zlabel is not None:
        ax.set_zlabel(zlabel)
    else:
        ax.set_zlabel(zunit)

    ax.xaxis.set_major_formatter(FormatStrFormatter(u'%.1f\N{DEGREE SIGN}E'))
    ax.yaxis.set_major_formatter(FormatStrFormatter(u'%.1f\N{DEGREE SIGN}N'))

    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    #ax.set_zlim(z.min(), 0)

    ax.view_init(elev=45, azim=-120)

    plt.show()
    #plt.savefig('3dview.png', bbox_inches='tight')

if __name__ == '__main__':

    ncfile = 'test/nc/ob500_avg.nc'

    #main(ncfile, 'oxygen', k=1)
    main(ncfile, 'h', zlabel='Depth (m)')

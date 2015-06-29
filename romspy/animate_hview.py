# -*- coding: utf-8 -*-

"""
2015/05/05 okada make this file from dynamic_images.py and hview.py.
"""

import netCDF4
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime

from basemap import basemap

class Hview(object):

    def __init__(self, ncfile, vname, k=None, vmax=None, vmin=None, 
                 interval=1, fmt='%i', cff=1.0, cblabel=None):
        self.nc = netCDF4.Dataset(ncfile, 'r')
        self.x_rho = self.nc.variables['lon_rho'][0,:]-0.00449/2
        self.y_rho = self.nc.variables['lat_rho'][:,0]-0.00546/2
        self.tunits = self.nc.variables['ocean_time'].units
        self.vname = vname
        self.k = k
        self.cff = cff
        self.ndim = len(self.nc.variables[vname].shape)
        if self.ndim is 4:
            var2d = self.nc.variables[vname][0,k-1,:,:] * cff
        if self.ndim is 3:
            var2d = self.nc.variables[vname][0,:,:] * cff

        self.X, self.Y = np.meshgrid(self.x_rho, self.y_rho)
        self.PC = plt.pcolor(self.X, self.Y, var2d)
        self.cbar = plt.colorbar(self.PC)
        self.cbar.ax.set_ylabel(cblabel)

    def __call__(self, t):

        self.ocean_time = self.nc.variables['ocean_time'][t]
        if self.ndim is 4:
            var2d = self.nc.variables[self.vname][t,self.k-1,:,:] * self.cff
        if self.ndim is 3:
            var2d = self.nc.variables[self.vname][t,:,:] * self.cff
        self.PC = plt.pcolor(self.X, self.Y, var2d)
        basemap()
        dtime = netCDF4.num2date(self.ocean_time, units=self.tunits)
        title = datetime.datetime.strftime(dtime,'%Y-%m-%d %H:%M:%S')
        plt.title(title)

        return self.PC,

if __name__ == '__main__':

    ncfile = '/home/work/okada/OB500/Biology_test_0/test_boundary/ob500_avg.nc'

    fig = plt.figure(figsize=(6,5))

    hview = Hview(ncfile, 'temp', k=1, cblabel='Temperature[C]')
    ani = animation.FuncAnimation(fig, hview, frames=np.arange(24), interval=1000,
                                  blit=True, repeat_delay=1000)
    plt.show()

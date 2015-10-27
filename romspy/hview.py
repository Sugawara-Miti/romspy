# -*- coding: utf-8 -*-

"""
(c) 2015-09-26 Teruhisa Okada
"""

import netCDF4
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime

from basemap import basemap

__version__ = 1.0
__version__ = 1.1  # 2015-10-26


class Dataset():
    JST = 'seconds since 1968-05-23 09:00:00 GMT'

    def __init__(self, ncfile, mapfile=None):
        print '\nDataset(ncfile={})'.format(ncfile)
        self.ncfile = ncfile
        self.mapfile = mapfile
        #self.vname = vname
        self.nc = netCDF4.Dataset(self.ncfile, 'r')

    def print_time(self, which='ends', name='ocean_time', tunit=JST):
        print "\nprint_time(which={}, name={}, tunit={})".format(which, name, tunit)
        nc = self.nc
        if which == 'ends':
            t = len(nc.dimensions[name])
            start = nc.variables[name][0]
            end = nc.variables[name][t-1]
            print netCDF4.num2date(start, tunit), 0
            print netCDF4.num2date(end, tunit), t-1
        elif which == 'all':
            time = nc.variables[name][:]
            for t in range(len(time)):
                print netCDF4.num2date(time[t], tunit), t
        else:
            print 'You should select "ends" or "all"'

    def print_varname(self, ndim=None):
        print '\nprint_varname(ndim={})'.format(ndim)
        if ndim is not None:
            for vname in self.nc.variables.keys():
                if self.nc.variables[vname].ndim == ndim:
                    print vname,
            print ''
        else:
            print self.nc.variables.keys()

    def get_varname(self, ndim=None):
        if ndim is not None:
            varnames = []
            for vname in self.nc.variables.keys():
                if self.nc.variables[vname].ndim == ndim:
                    varnames.append(vname)
            return varnames
        else:
            return self.nc.variables.keys()

    def hview(self, vname, time=-1, k=20, interval=None, fmt='%i', cff=1.0, 
              cblabel=None, cmap='jet', grdfile=None, tunit=JST):
        print 'hview(vname={}, time={}, k={}, interval={}, fmt={}, cff={}, cblabel={}, cmap={}, grdfile={}, tunit={})'.format(
            vname, time, k, interval, fmt, cff, cblabel, cmap, grdfile, tunit)
        nc = self.nc
        # read
        if grdfile is not None:
            grd = netCDF4.Dataset(grdfile, 'r')
            x_rho = grd.variables['lon_rho'][0,:]-0.00449/2
            y_rho = grd.variables['lat_rho'][:,0]-0.00546/2
            grd.close()
        else:
            x_rho = nc.variables['lon_rho'][0,:]-0.00449/2
            y_rho = nc.variables['lat_rho'][:,0]-0.00546/2

        if type(time) == datetime.datetime:
            t = netCDF4.date2num(time, tunit)
            ocean_time = nc.variables['ocean_time'][:]
            # print netCDF4.num2date(ocean_time[0], tunit), "-", netCDF4.num2date(ocean_time[-1], tunit)
            t = np.where(ocean_time==t)[0][0]
        elif type(time) == int:
            t = time
            time = netCDF4.num2date(nc.variables['ocean_time'][t], tunit)
        else:
            print 'ERROR: your type(time) is {}.\ntype(time) must be datetime.datetime or int\n'.format(type(time))

        var = nc.variables[vname]
        if var.ndim == 4:
            var2d = var[t,k-1,:,:] * cff
        elif var.ndim == 3:
            var2d = var[t,:,:] * cff
        else:
            var2d = var[:,:] * cff

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
        if self.mapfile is not None:
            basemap(self.mapfile)

        # finalize
        if vname == 'h':
            plt.title('Model domein & bathymetry')
        else:
            plt.title(datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S'))

        return ax

    def show(self):
        plt.show()

    def savefig(self, figfile='test.png'):
        plt.savefig(figfile, bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    ncfile = 'Z:/roms/Apps/OB500_fennelP/4DVAR04/output/ob500_ini_0.nc'
    mapfile = 'F:/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    ini = Dataset(ncfile, mapfile=mapfile)
    ini.print_time()
    ini.print_varname(4)
    time = 0
    k = 1
    #ini.hview('oxygen', time=time, k=k, interval=np.arange(0.0,300.1,50))
    #ini.savefig('hview_t{}_k{}.png'.format(time,k))

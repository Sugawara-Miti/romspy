# coding: utf-8
# (c) 2015-09-26 Teruhisa Okada

import netCDF4
import numpy as np
import datetime
import romspy


class Dataset():

    def __init__(self, ncfile, mapfile=None, grdfile=None):
        print '\nDataset(ncfile={})'.format(ncfile)
        self.ncfile = ncfile
        self.mapfile = mapfile
        self.grdfile = grdfile
        self.nc = netCDF4.Dataset(self.ncfile, 'r')
        self.X = None
        self.Y = None
        self.X2 = None
        self.Y2 = None

    def print_time(self, which='ends', name='ocean_time'):
        print "\nprint_time(which={}, name={}, tunit={})".format(which, name, romspy.JST)
        nc = self.nc
        if which == 'ends':
            t = len(nc.dimensions[name])
            start = nc.variables[name][0]
            end = nc.variables[name][t-1]
            print netCDF4.num2date(start, romspy.JST), 0
            print netCDF4.num2date(end, romspy.JST), t-1
        elif which == 'all':
            time = nc.variables[name][:]
            for t in range(len(time)):
                print netCDF4.num2date(time[t], romspy.JST), t
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

    def get_xy(self, method, step=1):
        """
        流速はそのまま，コンターは半グリッドずらしたxyを返す関数
        2015-11-08　作成
        """
        if self.X is None:
            if self.grdfile is not None:
                grd = netCDF4.Dataset(self.grdfile, 'r')
            else:
                grd = self.nc
            x_rho = grd.variables['lon_rho'][0,:]
            y_rho = grd.variables['lat_rho'][:,0]
            X, Y = np.meshgrid(x_rho, y_rho)
            self.X = X - 0.5 * (x_rho[1] - x_rho[0])
            self.Y = Y - 0.5 * (y_rho[1] - y_rho[0])
            self.X2 = X
            self.Y2 = Y

        if method == 'pcolor':
            return self.X, self.Y
        else:
            return self.X2[::step, ::step], self.Y2[::step, ::step]

    def get_time(self, time):
        if type(time) == datetime.datetime:
            t = netCDF4.date2num(time, romspy.JST)
            ocean_time = self.nc.variables['ocean_time'][:]
            t = np.where(ocean_time==t)[0][0]
        elif type(time) == int:
            t = time
            time = netCDF4.num2date(self.nc.variables['ocean_time'][t], romspy.JST)
        else:
            print 'ERROR: your type(time) is {}.\ntype(time) must be datetime.datetime or int\n'.format(type(time))
        return t, time

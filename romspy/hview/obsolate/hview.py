# coding: utf-8
# (c) 2015-09-26 Teruhisa Okada

import netCDF4
import matplotlib.pyplot as plt
import datetime
import numpy as np
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


class Hview(Dataset):

    def __init__(self, ncfile, mapfile=None, grdfile=None):
        Dataset.__init__(self, ncfile, mapfile, grdfile)

    def hview(self, vname, time=-1, k=20, fmt='%i', cff=None, unit='g', 
              cblabel=None, levels=None, step=3, scale=5, method='pcolor'):
        """
        2015-11-08　ベクトルに対応させるために ax_heatmap と ax_vecmap を追加
        """
        print '{}, time={}, k={}, fmt={},'.format(vname, time, k, fmt),

        if cff is None:
            cff = romspy.unit2cff(vname, unit)
        if levels is None:
            levels = romspy.levels(vname, unit)
        if cblabel is None:
            cblabel = vname
        print 'cff={}'.format(cff)

        if vname == 'velocity':
            var = self.nc.variables['u']
        else:
            var = self.nc.variables[vname]

        if var.ndim > 2:
            t, dtime = self.get_time(time)

        if vname == 'velocity':
            self.add_quiver(vname, t, k, cff, step, scale)
        else:
            if 'pcolor' in method:
                self.add_pcolor(vname, t, k, cff, levels, cblabel, fmt)
            if 'contour' in method:
                self.add_contour(vname, t, k, cff, levels, cblabel, fmt)
            if 'fill' in method:
                self.add_contourf(vname, t, k, cff, levels, cblabel, fmt)

        # basemap
        if self.mapfile is not None:
            romspy.basemap(self.mapfile)

        # print layer
        if k == 20:
            plt.text(135.25, 34.25, 'surface layer')
        elif k == 1:
            plt.text(135.25, 34.25, 'bottom layer')

        # finalize
        if var.ndim == 2:
            plt.title('Model domein & bathymetry')
        elif ('avg' in self.ncfile) or ('dia' in self.ncfile):
            time_string = datetime.datetime.strftime(dtime,'%Y-%m')
            plt.title('Average ({})'.format(time_string))
        else:
            plt.title(datetime.datetime.strftime(dtime,'%Y-%m-%d %H:%M:%S'))

        return plt.gca()

    def add_pcolor(self, vname, t, k, cff, levels, cblabel, fmt):
        """
        コンタープロットのaxを返す関数
        2015-11-08　作成
        """
        X, Y = self.get_xy('pcolor')
        var = self.nc.variables[vname]
        if var.ndim == 4:
            var2d = var[t,k-1,:,:] * cff
        elif var.ndim == 3:
            var2d = var[t,:,:] * cff
        else:
            var2d = var[:,:] * cff
        if levels is None:
            levels = romspy.levels(vname)

        ax = plt.gca()
        if levels is not None:
            P = ax.pcolor(X, Y, var2d, vmin=levels[0], vmax=levels[-1])
        else:
            P = ax.pcolor(X, Y, var2d)
        cbar = plt.colorbar(P)
        cbar.ax.set_ylabel(cblabel)
        return P

    def add_contour(self, vname, t, k, cff, levels, cblabel, fmt):
        """
        コンタープロットのaxを返す関数
        2015-11-08　作成
        """
        X, Y = self.get_xy('contour')
        var = self.nc.variables[vname]
        if var.ndim == 4:
            var2d = var[t,k-1,:,:] * cff
        elif var.ndim == 3:
            var2d = var[t,:,:] * cff
        else:
            var2d = var[:,:] * cff
        if levels is None:
            levels = romspy.levels(vname)

        ax = plt.gca()
        if levels is not None:
            C = ax.contour(X, Y, var2d, levels, colors='w')
        else:
            C = ax.contour(X, Y, var2d, colors='w')
        if fmt is not 'off':
            C.clabel(fmt=fmt, colors='k')  # ,fontsize=9)
        return C

    def add_contourf(self, vname, t, k, cff, levels, cblabel, fmt):
        """
        コンタープロットのaxを返す関数
        2015-11-08　作成
        """
        X, Y = self.get_xy('contour')
        var = self.nc.variables[vname]
        if var.ndim == 4:
            var2d = var[t,k-1,:,:] * cff
        elif var.ndim == 3:
            var2d = var[t,:,:] * cff
        else:
            var2d = var[:,:] * cff
        if levels is None:
            levels = romspy.levels(vname)

        ax = plt.gca()
        if levels is not None:
            F = ax.contourf(X, Y, var2d, levels, extend='both')
        else:
            F = ax.contourf(X, Y, var2d, extend='both')
        CB = plt.colorbar(F)
        CB.ax.set_ylabel(cblabel)
        return F

    def add_quiver(self, vname, t, k, cff, step, scale):
        """
        ベクトルの ax を返す関数
        2015-11-08　作成
        """
        X, Y = self.get_xy('quiver', step)
        if 'u_eastward' in self.nc.variables.keys():
            u = self.nc.variables['u_eastward'][t,k-1,::step,::step]
            v = self.nc.variables['v_northward'][t,k-1,::step,::step]
        else:
            u = self.nc.variables['u'][t,k-1,::step,::step]
            v = self.nc.variables['v'][t,k-1,::step,::step]

        ax = plt.gca()
        print X.shape, Y.shape, u.shape, v.shape
        if 'u_eastward' in self.nc.variables.keys():
            Q = ax.quiver(X, Y, u, v, units='width', angles='xy', scale=scale)
        else:
            Q = ax.quiver(X[:-1,:], Y[:-1,:], u[:-1,:], v, units='width', angles='xy', scale=scale)
        plt.quiverkey(Q, 0.9, 0.1, 1.0/scale, '1 m/s')
        return Q

    def show(self):
        plt.show()

    def savefig(self, figfile='test.png'):
        plt.savefig(figfile, bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    mapfile = '/home/okada/Dropbox/Maps/deg_OsakaBayMap_okada.bln'

    #ncfile = 'Z:/apps/OB500_fennelP/4DVAR04/output/ob500_ini_0.nc'
    ncfile = '/home/okada/apps/OB500P/case20/NL1/ob500_rst.nc'
    ini = Hview(ncfile, mapfile=mapfile)

    #ncfile = 'X:/2015_kaiko/trunk_NL_20120608_5/osaka-bay_avg.nc'
    #ncfile = 'X:/2015_kaiko/trunk_NL_20120608_5/osaka-bay_his_0017.nc'
    #grdfile = 'X:/2015_kaiko/Data/osaka-bay_grdfile_001.nc'
    #ini = Dataset(ncfile, mapfile=mapfile, grdfile=grdfile)
    #romspy.JST = 'seconds since 2012-06-01 00:00'

    ini.print_time('all')
    ini.print_varname(4)
    ini.hview('salt', time=-1, k=20)
    ini.hview('velocity', time=-1, k=20, step=3, scale=5)
    ini.show()
    #ini.savefig('hview_t{}_k{}.png'.format(time,k))

# coding: utf-8
# (c) 2016-02-10 Teruhisa Okada

import netCDF4
import numpy as np
import matplotlib.pyplot as plt

import romspy


class Grid():
        
    def __init__(self, grdfile):
        self.grdfile = grdfile
        nc = netCDF4.Dataset(self.grdfile, 'r')
        self.h = nc['h'][:]
        self.cs_r = nc['Cs_r'][:]
        x_rho = nc['lon_rho'][0,:]
        y_rho = nc['lat_rho'][:,0]
        nc.close()
        self.X, self.Y = np.meshgrid(x_rho, y_rho)


class Dataset(Grid):
    
    def __init__(self, ncfile, grdfile, mapfile):        
        Grid.__init__(self, grdfile)
        self.ncfile = ncfile
        self.mapfile = mapfile
        self.nc = netCDF4.Dataset(self.ncfile, 'r')

    def check_time(self, which='ends', name='ocean_time'):
        print "check_time(which={}, name={}, tunit={})".format(which, name, romspy.JST)
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

    def get_var(self, vname, t):
        zeta = self.nc['zeta'][t,:,:]
        var3d = self.nc[vname][t,:,:,:]
        N, M, L = var3d.shape
        dep3d = np.zeros_like(var3d)
        for n in range(N):
            dep3d[n,:,:] = self.cs_r[n] * (zeta + self.h)
        return var3d, dep3d

    def sview(self, vname, t, k, **kw):
        cff = kw.pop('cff', 1.0)
        var3d, dep3d = self.get_var(vname, t)
        S = var3d[k,:,:]*cff
        if k == 0:
            title = ' at {} layer'.format('bottom')
        elif k == 19:
            title = ' at {} layer'.format('surface')
        else:
            title = ' at {} layer'.format(k+1)
        self.hview(S, vname, t, title, **kw)

    def zview(self, vname, t, depth, **kw):
        cff = kw.pop('cff', 1.0)
        var3d, dep3d = self.get_var(vname, t)
        Z = romspy.zslice(var3d*cff, dep3d, depth)
        title = ' at {} m from surface'.format(depth)
        self.hview(Z, vname, t, title, **kw)

    def hview(self, var2d, vname, t, title, **kw):
        alpha = kw.pop('alpha', 0.5)
        fmt = kw.pop('fmt', '%i')  # %.1f
        label = kw.pop('label', None)
        contour = kw.pop('contour', True)
        contourf = kw.pop('contourf', True)
        clabel = kw.pop('clabel', True)
        linewidths = kw.pop('linewiths', 0.5)
        kw['extend'] = kw.pop('extend', 'both')
        
        ax = plt.gca()
        if contourf:
            CF = ax.contourf(self.X, self.Y, var2d, alpha=alpha, **kw)
            CB = plt.colorbar(CF)
        if contour:
            C = ax.contour(self.X, self.Y, var2d, colors='k', linewidths=linewidths, **kw)
        if clabel:
            C.clabel(colors='k', fmt=fmt)
        if label is not None:
            CB.ax.set_ylabel(label)
            title = label + title
        ax.set_title(title)
        romspy.basemap(self.mapfile)

if __name__ == '__main__':

    inifile = '/home/okada/ism-i/apps/OB500P/testDA/param5-001/output/ob500_ini_4800.nc'
    grdfile = '/home/okada/Data/ob500_grd-11_3.nc'
    mapfile = '/home/okada/romspy/romspy/deg_OsakaBayMap_okada.bln'
    
    nc = Dataset(inifile, grdfile, mapfile)
    nc.check_time()
    
    romspy.cmap('jet')

    kw = {}
    kw['levels'] = np.arange(9,31,1)
    kw['label'] = r'Temperature ($\degree$C)'
    
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    nc.sview(vname='temp', t=0, k=19, **kw)
    #nc.zview(vname='temp', t=0, depth=-1.0, **kw)

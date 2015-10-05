# -*- coding: utf-8 -*-

"""
profile class (c) 2015-09-26 Teruhisa Okada
"""

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
from romspy import O2_saturation


class Profile():
    sta_JST = 'seconds since 1968-05-23 09:00:00 GMT'
    obs_JST = 'days since 1968-05-23 09:00:00 GMT'

    def __init__(self, obsfile=None, freefile=None, assifile=None, t_obs=None, t_free=None, t_assi=None):
        self.obsfile = obsfile
        self.freefile = freefile
        self.assifile = assifile
        if obsfile is not None:
            self.obs = netCDF4.Dataset(obsfile, 'r')
            self.t_obs = t_obs
        if freefile is not None:
            self.free = netCDF4.Dataset(freefile, 'r')
            self.t_free = t_free
        if assifile is not None:
            self.assi = netCDF4.Dataset(assifile, 'r')
            self.t_assi = t_assi

    def calculate_depth(self, nc, t, station):
        s_rho = len(nc.dimensions['s_rho'])
        zeta = nc.variables['zeta'][t,station-1]
        h = nc.variables['h'][station-1]
        Cs_r = nc.variables['Cs_r'][:]
        depth = np.ndarray(shape=[s_rho])
        depth = (h + zeta) * Cs_r
        return depth

    def print_time(self, which='ends', name='ocean_time', tunit=sta_JST):
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

    def axes(self, x=1, y=1, figsize=[16,9]):
        fig, ax = plt.subplots(x, y, figsize=figsize)
        ax1 = [ax[i][j] for i in range(x) for j in range(y)]
        return ax1

    def plot_sta(self, ax, vname, station, date, label):
        print vname, station, date, label
        if label == 'Free':
            nc = self.free
            if self.t_free is None:
                ocean_time = nc.variables['ocean_time'][:]
                time = netCDF4.date2num(date, self.sta_JST)
                t = np.where(ocean_time == time)[0][0]
                self.t_free = t
            else:
                t = self.t_free
        elif label == 'Assi':
            nc = self.assi
            if self.t_assi is None:
                ocean_time = nc.variables['ocean_time'][:]
                time = netCDF4.date2num(date, self.sta_JST)
                t = np.where(ocean_time == time)[0][0]
                self.t_assi = t
            else:
                t = self.t_assi
        if vname == 'DIN':
            NH4 = nc.variables['NH4'][t,station-1,:]
            NO3 = nc.variables['NO3'][t,station-1,:]
            var = NH4 + NO3
        elif vname == 'PON':
            LDeN = nc.variables['LdetritusN'][t,station-1,:]
            SDeN = nc.variables['SdetritusN'][t,station-1,:]
            var = LDeN + SDeN
        elif vname == 'POP':
            LDeP = nc.variables['LdetritusP'][t,station-1,:]
            SDeP = nc.variables['SdetritusP'][t,station-1,:]
            var = LDeP + SDeP
        else:
            var = nc.variables[vname][t,station-1,:]
        depth = self.calculate_depth(nc, t, station)
        line = {'Free': '--', 'Assi': '-'}
        ax.plot(var, depth, line[label], label=label)

    def plot_obs(self, ax, vname, station, date, label):
        print vname, station, date, label
        nc = self.obs
        if self.t_obs is None:
            time = netCDF4.date2num(date, self.obs_JST)
            obs_time = nc.variables['obs_time'][:]
            index = np.where(obs_time == time)[0]
        else:
            index = self.t_obs
        obs_station = nc.variables['obs_station'][index]
        obs_type = nc.variables['obs_type'][index]
        obs_depth = nc.variables['obs_depth'][index]
        obs_value = nc.variables['obs_value'][index]
        data={'station':obs_station, 'depth':obs_depth, 'type':obs_type, 'value':obs_value}
        df = pd.DataFrame(data)
        df = df[df.station==station]
        varid = {'temp':6, 'salt':7, 'chlorophyll':10, 'oxygen':15}
        if vname in varid.keys():
            var = df[df.type == varid[vname]]
        elif vname == 'phytoplankton':
            var = df[df.type == varid['chlorophyll']]
            var.value = var.value / (Chl2C_m * PhyCN * C)
            var.value = var.value * 2.18
        else:
            return
        if vname == 'oxygen':
            T = df[df.type == varid['temp']]
            S = df[df.type == varid['salt']]
            T = np.asarray(T.value)
            S = np.asarray(S.value)
            O2p = np.asarray(var.value)
            var.value = O2p * O2_saturation(T, S) / 100.0
        ax.plot(var.value, var.depth, 'o', mec='k', mfc='w', mew=1, label=label)

    def plot(self, ax, vname, station, date):
        if self.freefile is not None:
            self.plot_sta(ax, vname, station, date, 'Free')
        if self.assifile is not None:
            self.plot_sta(ax, vname, station, date, 'Assi')
        if self.obsfile is not None:
            self.plot_obs(ax, vname, station, date, 'Obs')
        ax.grid()
        ax.set_ylim(-14,0)

    def show(self):
        plt.show()

    def savefig(self, figfile='test.png', bbox_inches='tight', dpi=300):
        plt.savefig(figfile, bbox_inches=bbox_inches, dpi=dpi)
        plt.close()


def test():
    freefile = 'Z:/roms/Apps/OB500_fennelP/NL09/ob500_sta.nc'
    obsfile = 'F:/okada/Dropbox/Data/ob500_obs_2012_obweb-3.nc'
    p = Profile(freefile=freefile, obsfile=obsfile)
    ax = p.axes(3,4,[16,9])
    time = dt.datetime(2012, 1, 10, 0)

    for i, station in enumerate([1,2,3,4,5,6,8,9,10,11,12,13]):
        p.plot(ax[i], 'temp', station, time)
        ax[i].set_xlim(0, 20)
        ax[i].set_title('Sta.{}'.format(station))
    p.show()


def fennelP(station, date, obsfile=None, freefile=None, assifile=None, t_assi=None):
    varnames = ['temp', 'salt', 'chlorophyll', 'oxygen', 'DIN', 'PON', 'PO4', 'POP']
    #colors = ['c', 'k', 'g', 'r', 'r', 'm', 'm', 'b']
    #c = {name:c for name, c in zip(varnames, colors)}
    p = Profile(obsfile=obsfile, freefile=freefile, assifile=assifile, t_assi=t_assi)
    ax = p.axes(2,4,[16,9])

    for i, vname in enumerate(varnames):
        p.plot(ax[i], vname, station, date)
        ax[i].set_title(vname)

    ax[0].set_xlim(0, 30)
    ax[1].set_xlim(15, 35)
    ax[2].set_xlim(0, 10)
    ax[3].set_xlim(0, 400)
    ax[4].set_xlim(0, 10)
    ax[5].set_xlim(0, 10)
    ax[6].set_xlim(0, 1)
    ax[7].set_xlim(0, 1)
    p.show()

if __name__ == '__main__':
    #test()
    freefile = 'Z:/roms/Apps/OB500_fennelP/NL07/ob500_sta.nc'
    assifile = 'Z:/roms/Apps/OB500_fennelP/4DVAR04/output/ob500_sta_0.nc'
    obsfile = 'F:/okada/Dropbox/Data/ob500_obs_2012_obweb-3.nc'
    from romspy import get_time
    print get_time(assifile, 'all')
    t_assi = 7
    fennelP(3, dt.datetime(2012, 8, 5, 0), obsfile=obsfile, freefile=freefile, assifile=assifile, t_assi=t_assi)

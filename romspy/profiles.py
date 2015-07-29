# coding: utf-8

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

sec_JST = 'seconds since 1968-05-23 09:00:00 GMT'
hour_JST = 'hours since 1968-05-23 09:00:00 GMT'


def read_sta(filename, pdt):

    print filename

    nc = netCDF4.Dataset(filename, 'r')
    station = len(nc.dimensions['station'])
    s_rho = len(nc.dimensions['s_rho'])
    h = nc.variables['h'][:]
    Cs_r = nc.variables['Cs_r'][:]
    ocean_time = nc.variables['ocean_time'][:]

    ptime = netCDF4.date2num(pdt, sec_JST)
    t = np.where(ocean_time == ptime)[0][0]

    print netCDF4.num2date(ocean_time[0], sec_JST), 0
    print pdt, t
    print netCDF4.num2date(ocean_time[-1], sec_JST), len(ocean_time)

    zeta = nc.variables['zeta'][t,:]
    depth = np.ndarray(shape=[station,s_rho])
    for n in range(s_rho):
        for sta in range(station):
            depth[sta, n] = (h[sta]+zeta[sta]) * Cs_r[n]
    return nc, t, depth


def plot_sta(vname, station, nc, t, depth, ax, label):

    var = nc.variables[vname]

    if vname == 'phytoplankton':
        cff = 1.0/0.2515/2.18
    else:
        cff = 1.0

    if label == 'Free': 
        line = '--'
    if label == 'Assi': 
        line = '-'

    c = {}
    c['temp'] = 'c'
    c['salt'] = 'k'
    c['phytoplankton'] = 'g'
    c['chlorophyll'] = 'g'
    c['NO3'] = 'r'
    c['NH4'] = 'b'
    c['PO4'] = 'm'
    c['oxygen'] = 'm'
    c['zooplankton'] = 'b'
    c['detritus'] = 'm'

    ax.plot(var[t,station-1,:]*cff, depth[station-1,:], line, c=c[vname], label=label)
    # ax.tick_params(labelleft='off')
    ax.set_ylim(-14,0)
    ax.set_title('Sta.{}'.format(station))
    ax.grid()


def read_obs(obsfile, pdt):

    print obsfile

    nc = netCDF4.Dataset(obsfile, 'r')
    ptime = netCDF4.date2num(pdt, hour_JST)
    obs_time = nc.variables['obs_time'][:]

    print netCDF4.num2date(obs_time[0], hour_JST), 0
    print pdt, ptime
    print netCDF4.num2date(obs_time[-1], hour_JST), len(obs_time)

    t = np.where(obs_time == ptime)[0]
    obs_station = nc.variables['obs_station'][t[0]:t[-1]]
    obs_type = nc.variables['obs_type'][t[0]:t[-1]]
    obs_depth = nc.variables['obs_depth'][t[0]:t[-1]]
    obs_value = nc.variables['obs_value'][t[0]:t[-1]]
    df = pd.DataFrame(data={'station':obs_station, 'depth':obs_depth, 'type':obs_type, 'value':obs_value})
    return df


def plot_obs(vname, station, obs, ax):

    cff = 1.0
    if vname == 'temp': 
        vid = 6
    elif vname == 'salt': 
        vid = 7
    elif vname == 'phytoplankton':
        vid = 10
        cff = 1.0/0.2515/2.18
    elif vname == 'chlorophyll':
        vid = 10
    elif vname == 'oxygen':
        vid = 15
    else:
        return

    var = obs[obs.station == station]
    var = var[var.type == vid]
    ax.plot(var.value*cff, var.depth, 'o', mec='k', mfc='w', mew=1, label='Obs')


def fennelP(pdt, station, free=None, assi=None, obs=None, png=None):

    if free is not None:
        free, ft, fdepth = read_sta(free, pdt)
    if assi is not None:
        assi, at, adepth = read_sta(assi, pdt)
    if obs is not None:
        obs = read_obs(obs, pdt)

    vnames = ['temp', 'salt', 'chlorophyll', 'NO3', 'NH4', 'PO4', 'oxygen']

    c = {}
    c['temp'] = 'c'
    c['salt'] = 'k'
    c['chlorophyll'] = 'g'
    c['NO3'] = 'r'
    c['NH4'] = 'b'
    c['PO4'] = 'm'
    c['oxygen'] = 'm'

    fig, ax = plt.subplots(1, len(vnames), figsize=[20,3])
    for i, vname in enumerate(vnames):
        if free is not None:
            plot_sta(vname, station, free, ft, fdepth, ax[i], 'Free')
        if assi is not None:
            plot_sta(vname, station, assi, at, adepth, ax[i], 'Assi')
        if obs is not None:
            plot_obs(vname, station, obs, ax[i])
        ax[i].grid()

    molN = u' [mmol N m$^{-3}$]'
    molP = u' [mmol P m$^{-3}$]'
    molO2 = u' [mmol O2 m$^{-3}$]'

    ax[0].set_xlabel('Temperature [degC]')
    ax[1].set_xlabel('Salinity')
    ax[2].set_xlabel('Chlorophyll [mg m$^{-3}$]')
    ax[3].set_xlabel('NO3'+molN)
    ax[4].set_xlabel('NH4'+molN)
    ax[5].set_xlabel('PO4'+molP)
    ax[6].set_xlabel('Oxygen'+molO2)

    ax[0].tick_params(labelleft='on')
    ax[0].set_xlim(23,33)
    ax[1].set_xlim(15,33)
    ax[2].set_xlim(0,20.0)
    ax[3].set_xlim(0,20.0)
    ax[4].set_xlim(0,2.0)
    ax[5].set_xlim(0,0.2)
    ax[6].set_xlim(0,300.0)

    strtime = pdt.strftime('%Y%m%d_%H%M')
    fig.savefig(png.format(station, strtime), bbox_inches='tight', dpi=300)


if __name__ == '__main__':

    pdt = dt.datetime(2012,2,24,0)
    station = 3
    free = '/Users/teruhisa/Dropbox/Data/OB500_fennelP/NL/ob500_sta.nc'
    obs = '/Users/teruhisa/Dropbox/Data/ob500_obs_2012_obweb-1.nc'
    png = '/Users/teruhisa/Dropbox/Data/OB500_fennelP/NL/profiles_{}_{}.png'
    fennelP(pdt, station, free=free, obs=obs, png=png)

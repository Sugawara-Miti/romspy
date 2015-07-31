# coding: utf-8

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

import romspy

sta_JST = 'seconds since 1968-05-23 09:00:00 GMT'
obs_JST = 'days since 1968-05-23 09:00:00 GMT'


def calculate_depth(nc, t, station):

    s_rho = len(nc.dimensions['s_rho'])
    zeta = nc.variables['zeta'][t,station-1]
    h = nc.variables['h'][station-1]
    Cs_r = nc.variables['Cs_r'][:]
    depth = np.ndarray(shape=[s_rho])
    depth = (h + zeta) * Cs_r

    return depth


def read_sta(stafile, dtime, station, varnames):

    nc = netCDF4.Dataset(stafile, 'r')
    ocean_time = nc.variables['ocean_time'][:]
    time = netCDF4.date2num(dtime, sta_JST)
    t = np.where(ocean_time == time)[0][0]
    var = {}
    for name in varnames:
        if name == 'TN':
            NH4 = nc.variables['NH4'][t,station-1,:]
            NO3 = nc.variables['NO3'][t,station-1,:]
            phyt = nc.variables['phytoplankton'][t,station-1,:]
            zoop = nc.variables['zooplankton'][t,station-1,:]
            LDeN = nc.variables['LdetritusN'][t,station-1,:]
            SDeN = nc.variables['SdetritusN'][t,station-1,:]
            var[name] = NH4 + NO3 + phyt + zoop + LDeN + SDeN
        elif name == 'TP':
            PO4 = nc.variables['PO4'][t,station-1,:]
            LDeP = nc.variables['LdetritusP'][t,station-1,:]
            SDeP = nc.variables['SdetritusP'][t,station-1,:]
            var[name] = PO4 + LDeP + SDeP
        elif name == 'PP':
            LDeP = nc.variables['LdetritusP'][t,station-1,:]
            SDeP = nc.variables['SdetritusP'][t,station-1,:]
            var[name] = LDeP + SDeP
        else:
            var[name] = nc.variables[name][t,station-1,:]

    print stafile
    print netCDF4.num2date(ocean_time[0], sta_JST), '-', netCDF4.num2date(ocean_time[-1], sta_JST)

    return var, calculate_depth(nc, t, station)


def read_obs(obsfile, dtime, station):

    nc = netCDF4.Dataset(obsfile, 'r')
    time = netCDF4.date2num(dtime, obs_JST)
    obs_time = nc.variables['obs_time'][:]

    print obsfile
    print netCDF4.num2date(obs_time[0], obs_JST), '-', netCDF4.num2date(obs_time[-1], obs_JST)

    index = np.where(obs_time == time)[0]
    obs_station = nc.variables['obs_station'][index]
    obs_type = nc.variables['obs_type'][index]
    obs_depth = nc.variables['obs_depth'][index]
    obs_value = nc.variables['obs_value'][index]
    data={'station':obs_station, 'depth':obs_depth, 'type':obs_type, 'value':obs_value}
    df = pd.DataFrame(data)
    df = df[df.station==station]

    return df


def plot_sta(varname, var, depth, ax, c, label):

    if varname == 'phytoplankton':
        cff = 1.0/0.2515/2.18
    else:
        cff = 1.0
    line = {'Free': '--', 'Assi': '-'}
    ax.plot(var[varname]*cff, depth, line[label], c=c[varname], label=label)
    # ax.tick_params(labelleft='off')


def plot_obs(varname, station, obs, ax):

    varid = {'temp':6, 'salt':7, 'chlorophyll':10, 'oxygen':15}

    if varname in varid.keys():
        var = obs[obs.type == varid[varname]]
    else:
        return
    if varname == 'oxygen':
        T = obs[obs.type == varid['temp']]
        S = obs[obs.type == varid['salt']]
        T = np.asarray(T.value)
        S = np.asarray(S.value)
        O2p = np.asarray(var.value)
        var.value = O2p * romspy.O2_saturation(T, S) / 100.0

    ax.plot(var.value, var.depth, 'o', mec='k', mfc='w', mew=1, label='Obs')


def fennelP(dtime, station, freefile=None, assifile=None, obsfile=None, pngfile=None):

    #varnames = ['temp', 'salt', 'chlorophyll', 'NO3', 'NH4', 'PO4', 'oxygen']
    #varnames = ['temp', 'salt', 'chlorophyll', 'TN', 'TP', 'PP', 'oxygen']
    varnames = ['temp', 'salt', 'chlorophyll', 'PO4', 'LdetritusP', 'SdetritusP', 'oxygen']
    colors = ['c', 'k', 'g', 'r', 'b', 'm', 'c']
    c = {name:c for name, c in zip(varnames, colors)}
    molN = u' [mmol N m$^{-3}$]'
    molP = u' [mmol P m$^{-3}$]'
    molO2 = u' [mmol O2 m$^{-3}$]'

    # read

    if freefile is not None:
        fvar, fdepth = read_sta(freefile, dtime, station, varnames)
    if assifile is not None:
        avar, adepth = read_sta(assifile, dtime, station, varnames)
    if obsfile is not None:
        obs = read_obs(obsfile, dtime, station)

    # plot

    fig, ax = plt.subplots(1, len(varnames), figsize=[20,3])
    for i, varname in enumerate(varnames):
        if freefile is not None:
            plot_sta(varname, fvar, fdepth, ax[i], c, 'Free')
        if assifile is not None:
            plot_sta(varname, avar, adepth, ax[i], c, 'Assi')
        if obsfile is not None:
            plot_obs(varname, station, obs, ax[i])
        ax[i].set_title('Sta.{}'.format(station))
        ax[i].grid()
        ax[i].set_ylim(-14,0)

    # settings

    ax[0].set_xlabel('Temperature [degC]')
    ax[1].set_xlabel('Salinity')
    ax[2].set_xlabel('Chlorophyll [mg m$^{-3}$]')
    #ax[3].set_xlabel('NO3'+molN)
    #ax[4].set_xlabel('NH4'+molN)
    #ax[5].set_xlabel('PO4'+molP)
    ax[3].set_xlabel('PO4'+molN)
    ax[4].set_xlabel('LDeP'+molP)
    ax[5].set_xlabel('SDeP'+molP)
    ax[6].set_xlabel('Oxygen'+molO2)

    ax[0].tick_params(labelleft='on')
    #ax[0].set_xlim(23,33)
    ax[1].set_xlim(15,33)
    ax[2].set_xlim(0,20.0)
    #ax[3].set_xlim(0,20.0)
    #ax[4].set_xlim(0,2.0)
    #ax[5].set_xlim(0,0.2)
    #ax[3].set_xlim(0,2.0)
    #ax[4].set_xlim(0,2.0)
    #ax[5].set_xlim(0,2.0)
    ax[6].set_xlim(0,500.0)

    # output

    if pngfile is not None:
        strtime = dtime.strftime('%m%d%H')
        fig.savefig(pngfile.format(station, strtime), bbox_inches='tight', dpi=300)
    else:
        return ax


if __name__ == '__main__':

    dtime = dt.datetime(2012,1,10,0)
    station = 12
    freefile = '/Users/teruhisa/Dropbox/Data/OB500_fennelP/NL03/ob500_sta.nc'
    obsfile = '/Users/teruhisa/Dropbox/Data/ob500_obs_2012_obweb-2.nc'
    pngfile = '/Users/teruhisa/Dropbox/Data/OB500_fennelP/NL03/profiles_{}_{}.png'

    fennelP(dtime, station, freefile=freefile, obsfile=obsfile, pngfile=pngfile)

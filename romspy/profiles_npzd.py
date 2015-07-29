# coding: utf-8

# import netCDF4
# import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
# import pandas as pd

from profiles import *

sec_JST = 'seconds since 1968-05-23 09:00:00 GMT'
hour_JST = 'hours since 1968-05-23 09:00:00 GMT'


def profiles_npzd(pdt, station, free=None, assi=None, obs=None, png=None):

    if free is not None:
        free, ft, fdepth = read_sta(free, pdt)
    if assi is not None:
        assi, at, adepth = read_sta(assi, pdt)
    if obs is not None:
        obs = read_obs(obs, pdt)

    vnames = ['temp', 'salt', 'phytoplankton', 'NO3', 'zooplankton', 'detritus']

    fig, ax = plt.subplots(1, len(vnames), figsize=[20,3])
    for i, vname in enumerate(vnames):
        if free is not None:
            plot_sta(vname, station, free, ft, fdepth, ax[i], 'Free')
        if assi is not None:
            plot_sta(vname, station, assi, at, adepth, ax[i], 'Assi')
        if obs is not None:
            plot_obs(vname, station, obs, ax[i])
        ax[i].grid()

    ax[0].tick_params(labelleft='on')
    mol = u' [mmol N m$^{-3}$]'

    ax[0].set_xlabel('Temperature [degC]')
    ax[1].set_xlabel('Salinity')
    ax[2].set_xlabel('Chlorophyll [mg m$^{-3}$]')
    ax[3].set_xlabel('NO3'+mol)
    ax[5].set_xlabel('Detritus'+mol)
    ax[4].set_xlabel('Zooplankton'+mol)

    ax[0].set_xlim(23,33)
    ax[1].set_xlim(15,33)
    # ax[2].set_xlim(0,20)
    # ax[3].set_xlim(0,0.5)
    ax[4].set_xlim(0,2.5)
    ax[5].set_xlim(0,2)

    fig.suptitle(pdt.strftime('%Y-%m-%d %H:%M'))
    strtime = pdt.strftime('%Y%m%d_%H%M')
    fig.savefig(png.format(station, strtime), bbox_inches='tight', dpi=300)


if __name__ == '__main__':

    pdt = dt.datetime(2012,8,24,0)
    station = 12
    free = '/Users/teruhisa/Dropbox/Data/mpi00_fujii/non_wq_runk_NL_20120608_5/osaka-bay_sta.nc'
    assi = '/Users/teruhisa/Dropbox/Data/mpi00_fujii/group_4dvar210_2_sta/osaka-bay_sta_024.nc'
    obs = '/Users/teruhisa/Dropbox/Data/ob500_obs_tsdc.nc'
    png = '/Users/teruhisa/Dropbox/0715_Lunch/profiles_{}_{}.png'
    profiles_npzd(pdt, station, free, assi, obs, png)

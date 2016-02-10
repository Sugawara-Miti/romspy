# coding: utf-8
# (c) 2015-11-25 Teruhisa Okada

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import netCDF4
import numpy as np
import pandas as pd
import datetime
import romspy

layers = {1:[1], 2:[1], 3:[1, 18], 4:[1, 14], 5:[0.7, 7.5],
           6:[1, 10], 8:[3.5, 12], 9:[6.5, 15], 10:[1, 6.1], 
           11:[1, 2.9], 12:[1, 10], 13:[1, 11]}
layers[13] = [1,10]


def tplot_valification(obsfile, modfile, varid, s, dates, **kw):
    layers = {1:[1], 2:[1], 3:[1, 18], 4:[1, 14], 5:[0.7, 7.5],
               6:[1, 10], 8:[3.5, 12], 9:[6.5, 15], 10:[1, 6.1], 
               11:[1, 2.9], 12:[1, 10], 13:[1, 11]}
    layers[13] = [1,10]
    layers = kw.pop('layers', layers)
    ax = kw.pop('ax', None)
    date_format = kw.pop('date_format', '%Y-%m')
    resample = kw.pop('resample', 'D')
    assimilation = kw.pop('assimilation', False)
    legend = kw.pop('legend', True)
    print obsfile, modfile, varid, s, dates

    obs = netCDF4.Dataset(obsfile, 'r')
    mod = netCDF4.Dataset(modfile, 'r')
    var = obs.variables
    time = var['obs_time'][:]
    type = var['obs_type'][:]
    station = var['obs_station'][:]
    layer = var['obs_layer'][:]

    index_type = (type==varid)
    index_station = (station==s)
    times = netCDF4.date2num(dates, romspy.JST_days)
    index_date = (times[0]<=time) & (time<times[-1])

    if ax is None:
        ax = plt.gca()

    for k in layers[s]:
        index = np.where(index_type & index_station & index_date & (layer==k))
        time = var['obs_time'][index]
        time = netCDF4.num2date(time, romspy.JST_days)
        obs_val = var['obs_value'][index]
        if assimilation:
            mod_val = mod.variables['NLmodel_initial'][index]
            mod_val_assim = mod.variables['NLmodel_value'][index]
        else:
            mod_val = mod.variables['NLmodel_value'][index]

        if varid == 15:
            cff = romspy.mol2g_O2
        else:
            cff = 1.0

        data = {'obs':obs_val*cff, 'model':mod_val*cff}
        if assimilation:
            data['assim'] = mod_val_assim*cff
        df = pd.DataFrame(data, index=time)
        df = df.dropna()
        df = df[df.model < 1000]
        loffset = {'M':'-15D', 'D':'-12H', 'H':'-30min'}
        df = df.resample(resample, how='mean', loffset=loffset[resample])
        colors = {layers[s][0]:'#4D71AF', layers[s][-1]:'#C34F53'}
        ax.plot(df.index.values, df.obs.values, '.-', lw=0.5, color=colors[k], label='obs ({})'.format(k))
        if assimilation:
            ax.plot(df.index.values, df.model.values, '--', lw=1.5, color=colors[k], label='background ({})'.format(k))
            ax.plot(df.index.values, df.assim.values, '-', lw=1.5, color=colors[k], label='assimilation ({})'.format(k))
        else:
            ax.plot(df.index.values, df.model.values, '-', lw=1.5, color=colors[k], label='mod ({})'.format(k))

    #ax.grid()
    if legend:
        ax.legend(loc='best')
    ax.set_title('Sta.{}'.format(s))
    ylabels = {6:'temperature [degC]', 7:'salinity', 10:'chlorophyll [mg/m3]', 15:'disolved oxygen [mg/l]'}
    ax.set_ylabel(ylabels[varid])
    ax.set_xlim(dates[0], dates[-1])
    ax.xaxis.set_major_formatter(DateFormatter(date_format))


def tplot_valification_3_2(obsfile, modfiles, varid, dates, **kw):
    stations = [3,4,5,6,12,13]
    fig, axes = plt.subplots(3, 2, figsize=[10,10])
    axlist = [axes[y][x] for x in range(2) for y in range(3)]
    for station, ax in zip(stations, axlist):
        tplot_valification(obsfile, modfile, varid, station, dates, ax=ax, legend=False, **kw)
    axlist[3].legend(bbox_to_anchor=(1.4, 1))
    plt.subplots_adjust(right=0.8)


def tplot_valification_6_1(obsfile, modfiles, varid, dates, **kw):
    stations = [3,4,5,6,12,13]
    fig, axes = plt.subplots(6, 1, figsize=[10,13])
    for station, ax in zip(stations, axes):
        for modfile in modfiles:
            tplot_valification(obsfile, modfile, varid, station, dates, ax=ax, legend=False, **kw)
        if varid == 6:
            ax.set_ylim(5, 30)
        elif varid == 7:
            ax.set_ylim(23, 33)
        elif varid == 10:
            ax.set_ylim(0, 30)
        elif varid == 15:
            ax.set_ylim(0, 12)
    axes[0].legend(bbox_to_anchor=(1.25, 1.1))
    plt.subplots_adjust(right=0.8, hspace=0.4)


def tplot_valification_1(obsfile, modfiles, varid, dates, station=12, **kw):
    fig, ax = plt.subplots(1, 1)
    for modfile in modfiles:
        tplot_valification(obsfile, modfile, varid, station, dates, ax=ax, legend=False, **kw)
    if varid == 6:
        ax.set_ylim(5, 30)
    elif varid == 7:
        ax.set_ylim(23, 33)
    elif varid == 10:
        ax.set_ylim(0, 30)
    elif varid == 15:
        ax.set_ylim(0, 12)
    #ax.legend(bbox_to_anchor=(1.25, 1.1))
    #plt.subplots_adjust(right=0.8)


if __name__ == '__main__':
    import seaborn as sns
    #obsfile = '/home/okada/Data/ob500_obs_2012_mp-1_ts.nc'
    #obsfile = '/home/okada/Data/ob500_obs_2012_mp-2.nc'
    obsfile = '/home/okada/Data/ob500_obs_2012_mp-3_clean.nc'
    #modfile = '/home/okada/ism-i/apps/OB500P/case28/DA0-3.1/output/ob500_mod_0.nc'
    modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/param4_0010_2/output/ob500_mod_{}.nc'.format(i*24) for i in range(0,7)]
    #modfiles = ['/home/okada/ism-i/apps/OB500P/case28/DA0-5.1/output/ob500_mod_{}.nc'.format(i*24) for i in range(0,7)]
    varid = 15
    #dates = [datetime.datetime(2012,8,3,0), datetime.datetime(2012,8,4,0)]
    #tplot_valification_3_2(obsfile, modfiles[0], varid, dates, date_format='%m/%d', resample='H', assimilation=True)
    dates = [datetime.datetime(2012,1,1,0), datetime.datetime(2012,1,8,0)]
    tplot_valification_6_1(obsfile, modfiles, varid, dates, date_format='%m/%d', resample='H', assimilation=True)
    #tplot_valification_1(obsfile, modfiles, varid, dates, date_format='%m/%d', resample='H', assimilation=True)
    plt.show()

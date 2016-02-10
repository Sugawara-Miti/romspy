# coding: utf-8
# (c) 2015-11-28 Teruhisa Okada

import netCDF4
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import pandas as pd
import romspy


def resample(date, var, **kw):
    rule = kw.pop('resample', 'D')
    if rule == 'H':
        loffset = '-30min'
    elif rule == 'D':
        loffset = '-12H'
    elif rule == 'M':
        loffset = '-15D'
    df = pd.DataFrame({'sur':var[:,-1], 'bot':var[:,0]}, index=date)
    df = df.resample(rule, loffset=loffset)
    return df.index.values, df.sur.values, df.bot.values


def tplot_station_main(stafile, vname, station, dates, **kw):
    print stafile, vname, station, dates
    ax = kw.pop('ax', None)
    date_format = kw.pop('date_format', '%Y-%m')
    cff = kw.pop('cff', 1.0)
    #ntime = kw.pop('ntime', 8785)

    if ax is None:
        ax = plt.gca()

    nc = netCDF4.Dataset(stafile, 'r')
    time = nc.variables['ocean_time']
    time = np.linspace(time[0], time[-1], len(time)) 
    date = netCDF4.num2date(time, romspy.JST)
    var = nc.variables[vname][:,station-1,[0,19]] * cff
    date, sur, bot = resample(date, var, **kw)

    ax.plot(date, sur, '-', lw=1.5, color='#4D71AF', label='surface')
    ax.plot(date, bot, '-', lw=1.5, color='#C34F53', label='bottom')
    ax.legend(loc='best')
    ax.set_title('Sta.{}'.format(station))
    ax.set_ylabel(vname)
    ax.set_xlim(dates[0], dates[-1])
    ax.xaxis.set_major_formatter(DateFormatter(date_format))


def tplot_station(stafile, vname, station, dates, **kw):
    if 'N' in vname:
        cff = romspy.mol2g_N
    elif 'P' in vname:
        cff = romspy.mol2g_P
    #elif 'plankton' in vname:
    #    cff = romspy.mol2g_N
    elif 'oxygen' in vname:
        cff = romspy.mol2g_O2
    else:
        cff = 1.0
    tplot_station_main(stafile, vname, station, dates, cff=cff, **kw)


if __name__ == '__main__':
    import seaborn as sns
    import datetime
    stafile = '/home/okada/ism-i/apps/OB500P/case25/NL2/ob500_sta.nc'
    vname = 'phytoplankton'
    stations = [3,4,5,6,12,13]
    dates = [datetime.datetime(2012,1,1,0), datetime.datetime(2013,1,1,0)]

    fig, axes = plt.subplots(6,1, figsize=[10,15])
    plt.subplots_adjust(hspace=0.4)
    for station, ax in zip(stations, axes):
        tplot_station(stafile, vname, station, dates, ax=ax, date_format='%m/%d')
        ax.set_ylim(-1,1)
    plt.show()

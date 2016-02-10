# coding: utf-8
# (c) 2015-11-28 Teruhisa Okada

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import netCDF4
import numpy as np
import pandas as pd
import romspy


def stick_plot_default(time, u, v, **kw):
    from matplotlib.dates import date2num
    #width = kw.pop('width', 0.002)
    #headwidth = kw.pop('headwidth', 0)
    #headlength = kw.pop('headlength', 0)
    #headaxislength = kw.pop('headaxislength', 0)
    angles = kw.pop('angles', 'uv')
    ax = kw.pop('ax', None)
    if angles != 'uv':
        raise AssertionError("Stickplot angles must be 'uv' so that"
                             "if *U*==*V* the angle of the arrow on"
                             "the plot is 45 degrees CCW from the *x*-axis.")
    uv = np.sqrt((u**2 + v**2))
    time, u, v, uv = map(np.asanyarray, (time, u, v, uv))
    if not ax:
        fig, ax = plt.subplots()
    q = ax.quiver(date2num(time), [[0]*len(time)], u, v, uv, angles='uv', 
                  #width=width, headwidth=headwidth,
                  #headlength=headlength, headaxislength=headaxislength,
                  **kw)
    ax.axes.get_yaxis().set_visible(False)
    ax.xaxis_date()
    return q


def stick_plot(time, u, v, **kw):
    from matplotlib.dates import date2num
    angles = kw.pop('angles', 'uv')
    ax = kw.pop('ax', None)
    if angles != 'uv':
        raise AssertionError("Stickplot angles must be 'uv' so that"
                             "if *U*==*V* the angle of the arrow on"
                             "the plot is 45 degrees CCW from the *x*-axis.")
    time, u, v = map(np.asanyarray, (time, u, v))
    if not ax:
        fig, ax = plt.subplots()
    q = ax.quiver(date2num(time), [[0]*len(time)], u, v, angles='uv', **kw)
    ax.axes.get_yaxis().set_visible(False)
    ax.xaxis_date()
    return q


def rolling_mean(date, u, v, hours):
    df = pd.DataFrame({'u':u, 'v':v}, index=date)
    df = pd.rolling_mean(df, window=hours, center=True)
    return date, df.u.values, df.v.values


def resample(date, u, v, **kw):
    rule = kw.pop('resample', 'D')
    if rule == 'H':
        loffset = '-30min'
    elif rule == '3H':
        loffset = '-1.5H'
    elif rule == '12H':
        loffset = '-6H'
    elif rule == 'D':
        loffset = '-12H'
    elif rule == 'M':
        loffset = '-15D'
    df = pd.DataFrame({'u':u, 'v':v}, index=date)
    df = df.resample(rule, loffset=loffset)
    print df
    #time = [dt64.astype('M8[s]').astype('O') for dt64 in df.index.values]
    return df.index.values.astype('M8[s]').astype('O'), df.u.values, df.v.values


def tplot_wind(ncfile, dates, x, y, **kw):
    print ncfile, dates, x, y, kw.keys()
    ax = kw.pop('ax', None)
    date_format = kw.pop('date_format', '%Y-%m')
    nc = netCDF4.Dataset(ncfile, 'r')
    try:
        time = nc.variables['time_wind'][:]
    except:
        time = nc.variables['wind_time'][:]
    date = netCDF4.num2date(time, romspy.JST_days)
    u = nc.variables['Uwind'][:,y,x]
    v = nc.variables['Vwind'][:,y,x]
    #date, u, v = rolling_mean(date, u, v, hours=hours)
    date, u, v = resample(date, u, v, **kw)
    q = stick_plot(date, u, v, ax=ax, width=0.002, scale=100, units='width')
    ax.set_xlim(dates[0], dates[-1])
    ax.xaxis.set_major_formatter(DateFormatter(date_format))
    ref = 5
    ref_str = "%s m s$^{-1}$" % ref
    ax.quiverkey(q, 0.1, 0.75, ref, ref_str, labelpos='N', coordinates='axes')


if __name__ == '__main__':
    from datetime import datetime
    import seaborn as sns
    ncfile = '/home/okada/Data/ob500_frc_wind_2012_rbf.nc'
    dates = [datetime(2012,1,1,0), datetime(2013,1,1,0)]
    dates = [datetime(2012,1,1,0), datetime(2012,1,7,0)]
    fig, ax = plt.subplots(figsize=(11, 2))
    #tplot_wind(ncfile, dates, 0, 0, hours=12, ax=ax)
    tplot_wind(ncfile, dates, 0, 0, resample='H', ax=ax)
    plt.show()
    #plt.savefig('check_wind.png')

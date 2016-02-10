# coding: utf-8
# (c) 2015-11-25 Teruhisa Okada

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import netCDF4
import numpy as np
import pandas as pd
import datetime
import os
import romspy


def tplot_rmse(obsfile, modfile, varid, s, layers=[0.5, 10], ax=None):
    print obsfile, modfile, varid, s, layers
    obs = netCDF4.Dataset(obsfile, 'r')
    var = obs.variables
    if modfile is not None:
        mod = netCDF4.Dataset(modfile, 'r')
    type = var['obs_type'][:]
    station = var['obs_station'][:]
    layer = var['obs_layer'][:]

    if ax is None:
        ax = plt.gca()
    for k in layers:
        index = np.where((type==varid) & (station==s) & (layer==k))
        time = var['obs_time'][index]
        time = netCDF4.num2date(time, romspy.JST_days)
        obs_val = var['obs_value'][index]
        mod_val = mod.variables['NLmodel_value'][index]
        data = {'obs':obs_val, 'model':mod_val}
        df = pd.DataFrame(data, index=time)
        df = df.dropna()
        df = df.resample('D', how='mean')
        ax.plot(df.index.values, df.obs.values, '.', label='obs (k={})'.format(k))
        ax.plot(df.index.values, df.model.values, '-', label='mod (k={})'.format(k))
    ax.legend(loc='best')
    ax.set_title('Sta.{}'.format(s))
    ax.set_xlim(datetime.date(2012,1,1), datetime.date(2013,1,1))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))


if __name__ == '__main__':

    import seaborn as sns
    import locale
    locale.setlocale(locale.LC_ALL, '')

    obsfile = '/home/okada/Data/ob500_obs_2012_mp-1.nc'
    modfile = '/home/okada/ism-i/apps/OB500P/case22/NL1/ob500_mod.nc'
    outdir  = os.path.dirname(modfile).replace('ism-i/apps', 'Dropbox/Figures')
    outfile_tmp = 'va_plot_{}.png'

    varid = 10
    stations = [3,4,5,6,12,13]
    layers = {1:[1], 2:[1], 3:[0.5, 18], 4:[0.5, 14], 5:[0.7, 7.5],
               6:[0.5, 10], 8:[3.5, 12], 9:[6.5, 15], 10:[1, 6.1], 
               11:[1, 2.9], 12:[0.5, 10], 13:[0.5, 11]}
    layers = {1:[1], 2:[1], 3:[1, 18], 4:[1, 14], 5:[0.7, 7.5],
               6:[1, 10], 8:[3.5, 12], 9:[6.5, 15], 10:[1, 6.1], 
               11:[1, 2.9], 12:[1, 10], 13:[1, 11]}

    print outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fig, axes = plt.subplots(3,2, figsize=[10,10])
    axlist = [axes[y][x] for x in range(2) for y in range(3)]
    for station, ax in zip(stations, axlist):
        tplot_valification(obsfile, varid, station, layers[station], modfile=modfile, ax=ax)

    plt.show()
    #outfile = os.path.join(outdir, outfile_tmp.format(varid))
    #romspy.savefig(outfile)

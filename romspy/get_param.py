# coding: utf-8
# (c) 2016-01-27 Teruhisa Okada

import netCDF4
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pandas as pd
import glob
import re
import romspy


def convert_param(inifiles, outfile):
    default = {}
    params = {}
    times = []
    for inifile in inifiles:
        print '\n', inifile,
        nc = netCDF4.Dataset(inifile, 'r')
        for vname in nc.variables.keys():
            if re.match(r'P\d\d', vname):
                print vname,
                param = nc[vname][:]
                if vname not in params.keys():
                    #default[vname] = param[-1]
                    params[vname] = param[::-1]
                else:
                    params[vname] = np.append(params[vname], param[0])
                if vname == 'P01':
                    time = nc['ocean_time'][:]
                    time = netCDF4.num2date(time, romspy.JST)
                    if len(times) == 0:
                        times.append(time[::-1])
                    else:
                        times = np.append(times, time[0])

    df = pd.DataFrame(params, index=times)
    print df
    df.to_csv(outfile)


def plot():
    fig, ax = plt.subplots(7,6,figsize=(12,12))
    axes = ax.flatten()
    for i in len(df.columns):
        vname = df.columns[i]
        ax[i].plot(df.index, df[vname].values, label=vname)

    plt.show()


def moving_avg(times, params, ax, window=3):
    df = pd.DataFrame(data={'param':params}, index=times)
    #df = df.resample('mean', )
    df = pd.rolling_mean(df, window=window, min_periods=1, center=True)
    ax.plot(df.index, df.param.values, '--', label='{}d-avg'.format(window))


def _get_files(tmpfile, hours):
    Nfiles = len(glob.glob(tmpfile))
    tmpfile = tmpfile.replace('*','{}')
    outfiles = [tmpfile.format(i) for i in range(0,hours*Nfiles,hours)]
    return outfiles


if __name__ == '__main__':
    import seaborn as sns

    test = 'param6-ini'
    hours = 24
    inifile_tmp = '/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_ini_*.nc'
    outfile = '/home/okada/Dropbox/Figures/2016_param/{}.csv'.format(test)

    inifiles = _get_files(inifile_tmp.format(test), hours=hours)
    convert_param(inifiles, outfile)

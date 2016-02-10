# coding: utf-8
# (c) 2016-01-27 Teruhisa Okada

import netCDF4
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pandas as pd
import glob
import romspy


def tplot_param(inifiles, vname, ax=plt.gca()):
    for inifile in inifiles:
        print inifile,
        nc = netCDF4.Dataset(inifile, 'r')
        param = nc[vname][:]
        #param = np.exp(param)
        time = nc['ocean_time'][:]
        time = netCDF4.num2date(time, romspy.JST)
        print time, param
        if 'params' not in locals():
            default = param[-1]
            params = param[0]
            times = time[0]
        else:
            params = np.append(params, param[0])
            times = np.append(times, time[0])

    ax.plot(times, params, 'o-', label='opt param')
    ax.set_ylabel(vname)
    ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))

    moving_avg(times, params, ax, window=3)
    moving_avg(times, params, ax, window=7)
    ax.legend()

    pmean = np.mean(params)
    pmedian = np.median(params)
    #ax.text(0.1,0.1,'mean={}'.format(pmean), transform=ax.transAxes)
    text = AnchoredText('mean={:.2e}'.format(pmean), loc=2)
    ax.add_artist(text)

    ax.plot([times[0], times[-1]], [default, default], '-', alpha=0.5, label='default')


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


def _plot6(inifiles):
    fig, ax = plt.subplots(6,1,figsize=(12,12))
    tplot_param(inifiles, 'P01', ax=ax[0])
    tplot_param(inifiles, 'P04', ax=ax[1])
    tplot_param(inifiles, 'P05', ax=ax[2])
    tplot_param(inifiles, 'P06', ax=ax[3])
    tplot_param(inifiles, 'P07', ax=ax[4])
    tplot_param(inifiles, 'P08', ax=ax[5])
    return ax


def _get_pfactor(test):
    if '0001' in test: 
        return 0.001
    elif '0005' in test:
        return 0.005
    elif '001' in test:
        return 0.01
    elif '005' in test:
        return 0.05
    elif '01' in test:
        return 0.1


def main(test, hours=24):
    inifiles = _get_files('/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_ini_*.nc'.format(test), hours=hours)
    figfile = '/home/okada/Dropbox/Figures/2016_param/tplot_param_{}.png'.format(test)
    if test == 'param2':
        fig, ax = plt.subplots(2,1)
        tplot_param(inifiles, 'P01', ax=ax[0])
        tplot_param(inifiles, 'P04', ax=ax[1])
        ax[0].set_title('4dvar(ini+param), window=1day, pfactor=0.1')
    elif 'param3' in test:
        ax = _plot6(inifiles)
        pfactor = _get_pfactor(test)
        ax[0].set_title('4dvar(ini+param), window=1day, pfactor={}'.format(pfactor))
    elif 'param4' in test:
        ax = _plot6(inifiles)
        pfactor = _get_pfactor(test)
        ax[0].set_title('4dvar(param), window=1day, pfactor={}'.format(pfactor))
    elif 'param5' in test:
        ax = _plot6(inifiles)
        pfactor = '*'
        ax[0].set_title('4dvar(ini+param), window=1day, pfactor={}'.format(pfactor))
    elif 'param6' in test:
        ax = _plot6(inifiles)
        pfactor = '*'
        ax[0].set_title('4dvar(param), window=7day, pfactor={}'.format(pfactor))
    romspy.savefig(figfile)
    #plt.show()


if __name__ == '__main__':
    import seaborn as sns
    #main('param5-05')
    #main('param5-01')
    #main('param5-005')
    #main('param5-001')
    #main('param5-01-hev')
    #main('param5-001-hev')
    #main('param5-001-7days', hours=24*7)
    #main('param6-p01-1', hours=24*7)
    #main('param6-p001-1', hours=24*7)
    #main('param6R-p01-7', hours=24*7)
    #main('param6R-p001-7', hours=24*7)
    main('param6-ini', hours=24)
    
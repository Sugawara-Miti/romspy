# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime as dt
import numpy as np
import netCDF4

def tview_obs(obsfile, pngfile=None, title=None, vname='chlorophyll', time=None):

    header = ['name','date','layer','depth','bottom','temp','salt','light','DO','turbidity','chlorophyll']

    if obsfile[-3:] == 'csv':
        try:
            df = pd.read_csv(obsfile, skiprows=[0], names=header, na_values='*')
            df = df[df[vname]>0]
            df.date = pd.to_datetime(df.date)

            pv = df.pivot(index='date', columns='layer', values=vname)
        except:
            df = pd.read_csv(obsfile, parse_dates=[['date','hour']],
                             na_values='*')
            pv = df.pivot(index='date_hour', columns='layer', values=vname)

        date = pv.index
        depth = pv.columns
        value = pv.values.T
        interval = np.arange(0,20,1)

    if obsfile[-2:] == 'nc':
        nc = netCDF4.Dataset(obsfile, 'r')
        tunit = nc.variables['survey_time'].units
        #start = netCDF4.date2num(time[0], tunit)
        #end = netCDF4.date2num(time[1], tunit)
        obs['type']

    plt.clf()
    fig, ax = plt.subplots(figsize=(10,4))

    cf = ax.contourf(date, -depth, value, interval, extend='max')
    cb = plt.colorbar(cf)
    cb.set_label(vname)
    if title is not None:
        ax.set_title(title)

    ax.set_xlabel('Aug 22-24, 2012')
    ax.set_xlim(dt.date(2012,8,22), dt.date(2012,8,24))
    ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )

    ax.set_ylabel('depth(m)')
    ax.set_ylim(-17, 0)

    if pngfile is not None:
        plt.savefig(pngfile.format(vname), bbox_inches='tight')

if __name__ == '__main__':

    test = 2
    if test == 0:
        tview_obs('4_kobe_wq_20120801_20120831.csv', '4_kobe_{}.png', 'Sta.4 Kobe')
        tview_obs('7_sakai_wq_20120801_20120831.csv', '7_sakai_{}.png', 'Sta.7 Sakai')
        tview_obs('12_osaka_wq_20120801_20120831.csv', '12_osaka_{}.png', 'Sta.12 Osaka')
    if test == 1:
        import datetime
        tview_obs('W:/Data/osaka-bay_chlo_201208_allpoints_outsaka_new_obs05.nc',
                  'osaka-bay_chlo_201208_allpoints_outsaka_new_obs05.png',
                  title='Chlorophyll',
                  time=[])
    if test == 2:
        tview_obs('/Users/teruhisa/Dropbox/Data/obweb/obweb/osaka_q1.csv')

# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime as dt
import numpy as np

def tview_obs_from_csv(csvfile, pngfile, title, vname='chlorophyll'):

    print csvfile, pngfile, title, vname

    header = ['name','date','layer','depth','bottom','temp','salt','light','DO','turbidity','chlorophyll']
    
    df = pd.read_csv(csvfile, skiprows=[0], names=header, na_values='*')
    df = df[df.chlorophyll>0]
    df.date = pd.to_datetime(df.date)
    
    pv = df.pivot(index='date', columns='layer', values=vname)

    plt.clf()
    fig, ax = plt.subplots(figsize=(10,4))

    date = pv.index
    depth = pv.columns
    value = pv.values.T
    interval = np.arange(0,20,1)
    
    cf = ax.contourf(date, -depth, value, interval, extend='max')
    cb = plt.colorbar(cf)
    cb.set_label(vname)
    ax.set_title(title)

    ax.set_xlabel('Aug 22-24, 2012')
    ax.set_xlim(dt.date(2012,8,22), dt.date(2012,8,24))
    ax.xaxis.set_major_formatter( DateFormatter('%H:%M') )

    ax.set_ylabel('depth(m)')
    ax.set_ylim(-17, 0)

    plt.savefig(pngfile.format(vname), bbox_inches='tight')

if __name__ == '__main__':

    tview_obs_from_csv('4_kobe_wq_20120801_20120831.csv', '4_kobe_{}.png', 'Sta.4 Kobe')
    tview_obs_from_csv('7_sakai_wq_20120801_20120831.csv', '7_sakai_{}.png', 'Sta.7 Sakai')
    tview_obs_from_csv('12_osaka_wq_20120801_20120831.csv', '12_osaka_{}.png', 'Sta.12 Osaka')

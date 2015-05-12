# -*- coding: utf-8 -*-

"""
2015/05/11 okada make this file.
"""

import netCDF4
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
import pandas as pd

def hplot_stations(obsfile):

    """
    You can use csv and nc file.
    """

    if obsfile[-3:] == 'csv':
        df = pd.read_csv(obsfile)
        print df
    elif obsfile[-2:] == 'nc':
        nc = netCDF4.Dataset(obsfile, 'r')
        obs = {}
        obs['lon'] = nc.variables['obs_lon'][:]
        obs['lat'] = nc.variables['obs_lat'][:]
        obs['station'] = nc.variables['obs_station'][:]
        df = pd.DataFrame(obs)
        df = df.drop_duplicates()
        print df
    else:
        print obsfile[-3:]
        pass
    
    plt.scatter(df.lon, df.lat, s=40, c='w', marker='o', lw=2)

    names = ['Sta.{}'.format(s) for s in df.station.values]
    bbox_props = dict(boxstyle="square", fc="w")

    """
    for x, y, name in zip(obs_lon, obs_lat, names):
        if name == 'Sta.4' or name == 'Sta.5' or name == 'Sta.12':
            plt.text(x-0.01, y-0.01, name, ha="right", va="top", bbox=bbox_props, fontsize=10)
    """

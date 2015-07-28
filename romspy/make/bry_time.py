# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

# import 

import netCDF4
import pandas as pd


def bry_time(dates=['2012-1-1', '2013-1-1'], bio_index=None):

    tunit_JST = 'days since 1968-05-23 09:00:00 GMT'

    time_h = pd.date_range(dates[0], dates[1], freq='H').to_pydatetime()
    time_d = pd.date_range(dates[0], dates[1], freq='D').to_pydatetime()
    time_a = [time_d[0], time_d[-1]]
    if bio_index is not None:
        time_b = bio_index.to_pydatetime()
    time_out = {}
    time_out['time_hourly']   = netCDF4.date2num(time_h, tunit_JST)
    time_out['time_daily']    = netCDF4.date2num(time_d, tunit_JST)
    time_out['time_annually'] = netCDF4.date2num(time_a, tunit_JST)
    if bio_index is not None:
        time_out['time_biology'] = netCDF4.date2num(time_b, tunit_JST)

    print time_out
    return time_out

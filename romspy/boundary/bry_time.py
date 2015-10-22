# coding: utf-8
# (c) 2015-10-14 Teruhisa Okada
# 2014/10/21 1.0
# 2015/10/14 2.0

import netCDF4
import pandas as pd

__version__ = 2.0


def bry_time(dates=['2012-1-1', '2013-1-1']):

    tunit_JST = 'days since 1968-05-23 09:00:00 GMT'

    time_h = pd.date_range(dates[0], dates[1], freq='H').to_pydatetime()
    time_d = pd.date_range(dates[0], dates[1], freq='D').to_pydatetime()
    time_a = [time_d[0], time_d[-1]]
    time_out = {}
    time_out['hourly']   = netCDF4.date2num(time_h, tunit_JST)
    time_out['daily']    = netCDF4.date2num(time_d, tunit_JST)
    time_out['annually'] = netCDF4.date2num(time_a, tunit_JST)

    print time_out
    return time_out

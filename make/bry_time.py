# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

# import 

import netCDF4
import pandas as pd

def bry_time(dates=['2012-1-1', '2013-1-1']):

    time_h = pd.date_range(dates[0], dates[1], freq='H').to_pydatetime()
    time_d = pd.date_range(dates[0], dates[1], freq='D').to_pydatetime()
    time_a = [time_d[0], time_d[-1]]
    
    time_out = {}
    time_out['time_hourly']   = [ netCDF4.date2num(t, 'days since 1968-05-23 09:00:00 GMT') for t in time_h ]
    time_out['time_daily']    = [ netCDF4.date2num(t, 'days since 1968-05-23 09:00:00 GMT') for t in time_d ]
    time_out['time_annually'] = [ netCDF4.date2num(t, 'days since 1968-05-23 09:00:00 GMT') for t in time_a ]
    
    return time_out

def bry_time_bio(dates, bio_index):
    
    time_out = bry_time(dates)
    
    time_b = bio_index.to_pydatetime()
    time_out['time_biology'] = [ netCDF4.date2num(t, 'days since 1968-05-23 09:00:00 GMT') for t in time_b ]
    
    return time_out
    

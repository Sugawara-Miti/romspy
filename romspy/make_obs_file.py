# -*- coding:utf-8 -*-

"""
2015/05/02 okada create this file.
2015/06/30 okada update.
"""

import netCDF4
import numpy as np
from numpy import dtype
from datetime import datetime
import pandas as pd


def make_obs_file(ncfile, csvfile, stafile, dates=None, varids=None):

    print 'ncfile:', ncfile
    print 'obsfile:', csvfile
    print 'stafile:', stafile
    print 'numpy version:', np.__version__, '(> 1.9.0)'

    GMT = 'days since 1968-05-23 00:00:00 GMT'
    JST = 'days since 1968-05-23 09:00:00 GMT'
    state_variable = 19

    df = pd.read_csv(csvfile, parse_dates=True, index_col='datetime')
    df = df.sort()
    if dates is not None:
        df = df[df.index >= dates[0]]
        df = df[df.index <= dates[1]]
    if varids is not None:
        if len(varids) == 2:
            df = df[(df.type==varids[0]) | (df.type==varids[1])]
    df.depth = -df.depth
    print df.head()
    print df.tail()
    #exit()

    """
    You need to change each errors
    """

    df['error'] = 0.0
    df.loc[df.type==6, "error"] = 0.5    # temp
    df.loc[df.type==7, "error"] = 0.5    # salt
    df.loc[df.type==10, "error"] = 1.0   # chlo
    df.loc[df.type==15, "error"] = 10.0  # oxygen

    df['xgrid'] = 0
    df['ygrid'] = 0
    df['lon'] = 0.0
    df['lat'] = 0.0
    sta = pd.read_csv(stafile, index_col='station')
    for i in xrange(1,14):
        df.ix[df.station==i, "xgrid"] = sta.xgrid[i]
        df.loc[df.station==i, "ygrid"] = sta.ygrid[i]
        df.loc[df.station==i, "lat"] = sta.lat[i]
        df.loc[df.station==i, "lon"] = sta.lon[i]

    time = [ts.to_datetime() for ts in df.index.tolist()]
    time_out = netCDF4.date2num(time, JST)
    survey_out, nobs_out = np.unique(time_out, return_counts=True)

    station_out = df.station.tolist()
    depth_out = df.depth.tolist()
    type_out = df.type.tolist()
    value_out = df.value.tolist()
    xgrid_out = df.xgrid.tolist()
    ygrid_out = df.ygrid.tolist()
    lon_out = df.lon.tolist()
    lat_out = df.lat.tolist()
    error_out = df.error.tolist()

    """
    write netcdf
    """

    nc = netCDF4.Dataset(ncfile, 'w', format='NETCDF3_CLASSIC')

    now = datetime.now()
    nc.history = now.strftime('%Y-%m-%d %H:%M:%S')
    nc.author = 'OKADA Teruhisa'

    nc.createDimension('survey', len(survey_out))
    nc.createDimension('state_variable', state_variable)
    nc.createDimension('datum', sum(nobs_out))
    for name in nc.dimensions.keys():
        print nc.dimensions[name]

    spherical = nc.createVariable('spherical', dtype('int32').char)
    spherical.long_name = 'grid type logical seitch'
    spherical.flag_values = [0, 1]
    spherical.flag_meanings = 'Cartesian Spherical'

    Nobs = nc.createVariable('Nobs', dtype('int32').char, ('survey',))
    Nobs.long_name = 'number of observations with the same survey time'

    survey_time = nc.createVariable('survey_time', dtype('double').char, ('survey',))
    survey_time.long_name = 'survey time'
    survey_time.units = GMT
    survey_time.calendar = 'gregorian'

    obs_variance = nc.createVariable('obs_variance', dtype('double').char, ('state_variable',))
    obs_variance.long_name = 'global time and space observation variance'

    obs_type = nc.createVariable('obs_type', dtype('int32').char, ('datum',))
    obs_type.long_name = 'model state variable associated with observation'
    obs_type.flag_values = [i + 1 for i in range(16)]
    obs_type.flag_meanings = 'zeta ubar vbar u v temperature salinity NO3 phytoplankton zooplankton detritus'

    obs_provenance = nc.createVariable('obs_provenance', dtype('int32').char, ('datum',))
    obs_provenance.long_name = 'observation origin'
    obs_provenance.flag_values = [1]
    obs_provenance.flag_meanings = 'OBWQ13'

    obs_station = nc.createVariable('obs_station', dtype('int32').char, ('datum',))
    obs_station.long_name = 'observation station number'
    obs_station.flag_values = [i+1 for i in range(13)]
    obs_station.flag_meanings = 'akashi sumoto kanku kobe yodo hannan sakai rokko hamadera awaji suma osaka kishiwada'

    obs_time  = nc.createVariable('obs_time', dtype('double').char, ('datum',))
    obs_depth = nc.createVariable('obs_depth', dtype('double').char, ('datum',))
    obs_Xgrid = nc.createVariable('obs_Xgrid', dtype('double').char, ('datum',))
    obs_Ygrid = nc.createVariable('obs_Ygrid', dtype('double').char, ('datum',))
    obs_Zgrid = nc.createVariable('obs_Zgrid', dtype('double').char, ('datum',))
    obs_lon   = nc.createVariable('obs_lon', dtype('double').char, ('datum',))
    obs_lat   = nc.createVariable('obs_lat', dtype('double').char, ('datum',))
    obs_error = nc.createVariable('obs_error', dtype('double').char, ('datum',))
    obs_value = nc.createVariable('obs_value', dtype('double').char, ('datum',))

    obs_time.long_name  = 'time of observation'
    obs_time.units      = GMT
    obs_time.calendar   = 'gregorian'
    obs_depth.long_name = 'depth of observation'
    obs_depth.units     = 'meter'
    obs_depth.negative  = 'downwards'
    obs_Xgrid.long_name = 'observation fractional x-grid location'
    obs_Ygrid.long_name = 'observation fractional y-grid location'
    obs_Zgrid.long_name = 'observation fractional z-grid location'
    obs_lon.long_name   = 'observation longitude'
    obs_lat.long_name   = 'observation latitude'
    obs_error.long_name = 'observation error covariance'
    obs_value.long_name = 'observation value'

    spherical[:] = 1
    Nobs[:] = nobs_out
    survey_time[:] = survey_out
    obs_variance[:] = 0
    obs_provenance[:] = 0

    obs_time[:] = time_out
    obs_type[:]  = type_out
    obs_depth[:] = depth_out
    obs_Xgrid[:] = xgrid_out
    obs_Ygrid[:] = ygrid_out
    obs_Zgrid[:] = 0
    obs_station[:] = station_out
    obs_lon[:]   = lon_out
    obs_lat[:]   = lat_out
    obs_error[:] = error_out
    obs_value[:] = value_out

    for name in nc.variables.keys():
        print name, nc.variables[name][:]

    nc.close()
    print 'Finish!'


if __name__ == '__main__':

    outfile = '/Users/teruhisa/Dropbox/Data/ob500_obs_201208_bio-1.nc'
    inpfile = '/Users/teruhisa/Dropbox/Data/obweb/converted_db.csv'
    stafile = '/Users/teruhisa/Dropbox/Data/stations13.csv'
    dates = [datetime(2012,8,1,0), datetime(2012,9,1,0)]
    varids = [10,15]
    make_obs_file(outfile, inpfile, stafile, dates, varids)

# coding: utf-8
# (c) 2015-05-02 Teruhisa Okada

"""
2015/05/02 okada create this file.
2015/06/30 okada update.
# (c) 2015-11-24 Teruhisa Okada
"""

import netCDF4
import numpy as np
from numpy import dtype
from datetime import datetime
import pandas as pd
import romspy


def make_obs_file(ncfile, csvfile, stafile=None, dates=None, varids=None, flag=1, e=None):

    print 'ncfile:', ncfile
    print 'obsfile:', csvfile
    print 'stafile:', stafile
    print 'numpy version:', np.__version__, '(> 1.9.0)'

    state_variable = 19

    df = pd.read_csv(csvfile, parse_dates=['date'], index_col='date')
    df = df.sort()
    print df
    if dates is not None:
        df = df[df.index >= dates[0]]
        df = df[df.index <= dates[1]]
    if varids is not None:
        if len(varids) == 2:
            df = df[(df.type==varids[0]) | (df.type==varids[1])]
    print df.head()
    print df.tail()

    """
    You need to change each errors
    """

    df['error'] = 0.0

    if flag == 1:  # OBWQ13
        df.depth = -df.depth
        if e is None:
            df.loc[df.type==6, "error"] = 0.5 + 0.005    # temp
            df.loc[df.type==7, "error"] = 0.5 + 0.005    # salt
            df.loc[df.type==10, "error"] = 1.0 + 0.05    # chlo
            df.loc[df.type==15, "error"] = 10.0 + 0.05   # oxygen
        else:
            df.loc[df.type==6, "error"] = e[0]    # temp
            df.loc[df.type==7, "error"] = e[1]    # salt
            df.loc[df.type==10, "error"] = e[2]    # chlo
            df.loc[df.type==15, "error"] = e[3]   # oxygen
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
    elif flag == 2:  # OB_RADAR
        df.loc[df.type==4, "error"] = 0.05           # u
        df.loc[df.type==5, "error"] = 0.05           # v
        df['depth'] = -0.5
        df['station'] = 0
        df['layer'] = 0.5

    if type(df.index.values[0]) == str:
        time = datetime.strptime(df.index.values, '')
    elif type(df.index.values[0]) == np.datetime64:
        time = [dt64.astype('M8[s]').astype('O') for dt64 in df.index.values]
    else:
        time = [ts.to_datetime() for ts in df.index.values]
        print type(df.index.values[0]), df.index.values[0]
    time_out = netCDF4.date2num(time, romspy.JST_days)
    survey_out, nobs_out = np.unique(time_out, return_counts=True)

    station_out = df.station.values
    layer_out = df.layer.values
    depth_out = df.depth.values
    type_out = df.type.values
    value_out = df.value.values
    xgrid_out = df.xgrid.values
    ygrid_out = df.ygrid.values
    lon_out = df.lon.values
    lat_out = df.lat.values
    error_out = df.error.values

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
    spherical.flag_ncfile_tru = [0, 1]
    spherical.flag_meanings = 'Cartesian Spherical'

    Nobs = nc.createVariable('Nobs', dtype('int32').char, ('survey',))
    Nobs.long_name = 'number of observations with the same survey time'

    survey_time = nc.createVariable('survey_time', dtype('double').char, ('survey',))
    survey_time.long_name = 'survey time'
    survey_time.units = romspy.GMT_days
    survey_time.calendar = 'gregorian'

    obs_variance = nc.createVariable('obs_variance', dtype('double').char, ('state_variable',))
    obs_variance.long_name = 'global time and space observation variance'

    obs_type = nc.createVariable('obs_type', dtype('int32').char, ('datum',))
    obs_type.long_name = 'model state variable associated with observation'
    obs_type.flag_values = [i + 1 for i in range(16)]
    obs_type.flag_meanings = '1:zeta 2:ubar 3:vbar 4:u 5:v 6:temperature 7:salinity 8:NH4 9:NO3 10:chlorophyll 11:phytoplankton 12:zooplankton 13:LdetritusN 14:SdetritusN 15:oxygen 16:PO4 17:LdetritusP 18:SdetritusP 19:H2S'

    obs_provenance = nc.createVariable('obs_provenance', dtype('int32').char, ('datum',))
    obs_provenance.long_name = 'observation origin'
    obs_provenance.flag_values = [1, 2]
    obs_provenance.flag_meanings = '1:OBWQ13 2:OB_RADAR'

    obs_station = nc.createVariable('obs_station', dtype('int32').char, ('datum',))
    obs_station.long_name = 'observation station number'
    obs_station.flag_values = [i+1 for i in range(13)]
    obs_station.flag_meanings = 'akashi sumoto kanku kobe yodo hannan sakai rokko hamadera awaji suma osaka kishiwada'

    obs_time  = nc.createVariable('obs_time', dtype('double').char, ('datum',))
    obs_layer = nc.createVariable('obs_layer', dtype('double').char, ('datum',))
    obs_depth = nc.createVariable('obs_depth', dtype('double').char, ('datum',))
    obs_Xgrid = nc.createVariable('obs_Xgrid', dtype('double').char, ('datum',))
    obs_Ygrid = nc.createVariable('obs_Ygrid', dtype('double').char, ('datum',))
    obs_Zgrid = nc.createVariable('obs_Zgrid', dtype('double').char, ('datum',))
    obs_lon   = nc.createVariable('obs_lon', dtype('double').char, ('datum',))
    obs_lat   = nc.createVariable('obs_lat', dtype('double').char, ('datum',))
    obs_error = nc.createVariable('obs_error', dtype('double').char, ('datum',))
    obs_value = nc.createVariable('obs_value', dtype('double').char, ('datum',))

    obs_time.long_name  = 'time of observation'
    obs_time.units      = romspy.GMT_days
    obs_time.calendar   = 'gregorian'
    obs_layer.long_name = 'layer of observation'
    obs_layer.units     = 'nondimensional'
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
    obs_provenance[:] = flag

    obs_time[:] = time_out
    obs_type[:]  = type_out
    obs_layer[:] = layer_out
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

    dates = [datetime(2012,1,1,0), datetime(2013,1,1,0)]
    varids = None
    stafile = '/home/okada/Dropbox/Data/stations13.csv'
    flag = 1
    errors = None
    outfile_tmp = '/home/okada/Data/ob500_obs_2012_{}.nc'

    name = 'mp-3_clean'

    if name == 'obweb-5':
        outfile = 'F:/okada/Dropbox/Data/ob500_obs_2012_obweb-5.nc'
        inpfile = 'Z:/Data/obweb/converted_db_oxygen3.csv'
        stafile = 'Z:/Data/stations13.csv'

    elif name == 'mp-1':
        outfile = outfile_tmp.format(name)
        inpfile = '/home/okada/Data/mp/converted_mp.csv'

    elif name == 'mp-1_ts':
        outfile = outfile_tmp.format(name)
        inpfile = '/home/okada/Data/mp/converted_mp.csv'
        varids = [6, 7]

    elif name == 'mp-1_bio':
        outfile = outfile_tmp.format(name)
        inpfile = '/home/okada/Data/mp/converted_mp.csv'
        varids = [10, 15]

    elif name == 'mp-2':
        outfile = outfile_tmp.format(name)
        inpfile = '/home/okada/Data/mp/converted_mp-2.csv'

    elif name == 'radar-1':
        flag = 2
        inpfile = 'Z:/Data/radar/converted_radar_20120201_20120301.csv'
        outfile = 'Z:/Data/ob500_obs_2012_{}.nc'.format(name)
        varids = [4, 5]
        stafile = None

    elif name == 'mp-3':
        outfile = outfile_tmp.format(name)
        inpfile = '/home/okada/Data/mp/converted_mp-2.csv'
        errors = [0.34, 0.21, 7.53, 14.19]  # Sakai, 2011
        errors[2] = 11.47  # obs by ship, 2015

    elif name == 'mp-3_clean':
        outfile = outfile_tmp.format(name)
        inpfile = '/home/okada/Data/mp/converted_mp-2_clean.csv'
        errors = [0.34, 0.21, 7.53, 14.19]  # Sakai, 2011
        errors[2] = 11.47  # obs by ship, 2015

    make_obs_file(outfile, inpfile, stafile, dates, varids=varids, flag=flag, e=errors)

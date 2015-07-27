# -*- coding:utf-8 -*-

"""
2015/05/02 okada create this file.
"""

import shutil
import netCDF4
import numpy as np
from numpy import dtype
import datetime

def make_obs_file(ncfile):

    tunit = 'days since 1968-05-23 00:00:00'
    vari_out = [1 for _ in range(11)]
    surv_out = [t for t in range(10)]
    nobs_out = [1 for _ in range(10)]

    nc = netCDF4.Dataset(ncfile, 'w', format='NETCDF3_CLASSIC')

    now = datetime.datetime.now()
    nc.history = now.strftime('%Y-%m-%d %H:%M:%S')
    nc.author = 'OKADA Teruhisa'

    nc.createDimension('survey',         len(surv_out))
    nc.createDimension('state_variable', len(vari_out))
    nc.createDimension('datum',          sum(nobs_out))
    for name in nc.dimensions.keys():
        print nc.dimensions[name]

    spherical = nc.createVariable('spherical', dtype('int32').char )
    spherical.long_name = 'grid type logical seitch'
    spherical.flag_values = [0, 1]
    spherical.flag_meanings = 'Cartesian Spherical'
    
    Nobs = nc.createVariable('Nobs', dtype('int32').char, ('survey',) )
    Nobs.long_name = 'number of observations with the same survey time'
    
    survey_time = nc.createVariable('survey_time', dtype('double').char, ('survey',) )
    survey_time.long_name = 'survey time'
    survey_time.units = tunit
    survey_time.calendar = 'gregorian'
    
    obs_variance = nc.createVariable('obs_variance', dtype('double').char, ('state_variable',) )
    obs_variance.long_name = 'global time and space observation variance'
    
    obs_type = nc.createVariable('obs_type', dtype('int32').char, ('datum',) )
    obs_type.long_name = 'model state variable associated with observation'
    obs_type.flag_values = [1,2,3,4,5,6,7,8,9,10,11]
    obs_type.flag_meanings = 'zeta ubar vbar u v temperature salinity NO3 phytoplankton zooplankton detritus'
    
    obs_provenance = nc.createVariable('obs_provenance', dtype('int32').char, ('datum',) )
    obs_provenance.long_name = 'observation origin'
    obs_provenance.flag_values = [1]
    obs_provenance.flag_meanings = 'OBWQ13'
    
    obs_station = nc.createVariable('obs_station', dtype('int32').char, ('datum',) )
    obs_station.long_name = 'observation station number'
    obs_station.flag_values = [i+1 for i in range(13)]
    obs_station.flag_meanings = 'akashi sumoto kanku kobe yodo hannan sakai rokko hamadera awaji suma osaka kishiwada'

    obs_time  = nc.createVariable('obs_time', dtype('double').char, ('datum',) )
    obs_depth = nc.createVariable('obs_depth', dtype('double').char, ('datum',) )
    obs_Xgrid = nc.createVariable('obs_Xgrid', dtype('double').char, ('datum',) )
    obs_Ygrid = nc.createVariable('obs_Ygrid', dtype('double').char, ('datum',) )
    obs_Zgrid = nc.createVariable('obs_Zgrid', dtype('double').char, ('datum',) )
    obs_lon   = nc.createVariable('obs_lon', dtype('double').char, ('datum',) )
    obs_lat   = nc.createVariable('obs_lat', dtype('double').char, ('datum',) )
    obs_error = nc.createVariable('obs_error', dtype('double').char, ('datum',) )
    obs_value = nc.createVariable('obs_value', dtype('double').char, ('datum',) )

    obs_time.long_name  = 'time of observation'
    obs_time.units      = tunit
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

    spherical[:] = 0
    Nobs[:] = nobs_out
    survey_time[:] = surv_out
    obs_variance[:] = vari_out
    obs_provenance[:] = 1

    obs_time[:] = surv_out
    obs_type[:]  = 6
    obs_depth[:] = -100.0
    obs_Xgrid[:] = 2
    obs_Ygrid[:] = 2
    obs_Zgrid[:] = 0
    obs_station[:] = 1
    obs_lon[:]   = 0
    obs_lat[:]   = 0
    obs_error[:] = 0.1
    obs_value[:] = 4.1

    for name in nc.variables.keys():
        print name, nc.variables[name][:]

    nc.close()
    print 'Finish!'
    
if __name__ == '__main__':

    make_obs_file('bio_toy_obs.nc')

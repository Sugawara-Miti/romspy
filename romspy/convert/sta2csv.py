
# coding: utf-8

# In[1]:

import netCDF4
import numpy as np
import pandas as pd

def sta2csv(ncfiles, csvfile):
    
    nc      = netCDF4.MFDataset(ncfiles, 'r')
    names   = nc.variables.keys()

    flux = {}

    for name in names:
        if nc.variables[name].ndim == 2:
            print name, nc.variables[name].ndim
            flux[name] = nc.variables[name][:,:].flatten()
            
    nt    = len(nc.dimensions['ocean_time'])
    nsta  = len(nc.dimensions['station'])
    tunit = nc.variables['ocean_time'].units

    #

    time = np.zeros_like(nc.variables['zeta'][:,:])
    lon  = np.zeros_like(nc.variables['zeta'][:,:])
    lat  = np.zeros_like(nc.variables['zeta'][:,:])
    sta  = np.zeros_like(nc.variables['zeta'][:,:])

    for t in xrange(nt):
        time[t,:] = nc.variables['ocean_time'][t]
        
    for s in xrange(nsta):
        lon[:,s] = nc.variables['lon_rho'][s]
        lat[:,s] = nc.variables['lat_rho'][s]
        sta[:,s] = s + 1
        
    flux['time']    = time.flatten()
    flux['lon']     = lon.flatten()
    flux['lat']     = lat.flatten()
    flux['station'] = sta.flatten()

    #

    df = pd.DataFrame(flux)

    num2date = lambda num: netCDF4.num2date(num, tunit)
    df.time  = df.time.apply(num2date)
    df       = df.set_index(['time','lon','lat','station'])

    df.to_csv(csvfile)

if __name__ == '__main__':

    ncfiles = ['../roms2-1/ob500_sta.nc',
               '../roms2-2/ob500_sta.nc',
               '../roms2-3/ob500_sta.nc',
               '../roms2-4/ob500_sta.nc']

    csvfile = 'sta.csv'
    
    sta2csv(ncfiles, csvfile)

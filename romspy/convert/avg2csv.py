
# coding: utf-8

# In[8]:

import netCDF4
import numpy as np
import pandas as pd

def avg2csv(ncfile, csvname):

    print ncfile, csvname

    nc    = netCDF4.MFDataset(ncfile, 'r')
    names = nc.variables.keys()

    flux = {}

    for name in names:
        if nc.variables[name].ndim == 3:
            flux[name] = nc.variables[name][:,:,:].flatten()

    nt = len(nc.dimensions['ocean_time'])
    nx = len(nc.dimensions['xi_rho'])
    ny = len(nc.dimensions['eta_rho'])
    tunit = nc.variables['ocean_time'].units

    #

    time = np.zeros_like(nc.variables['zeta'][:,:,:])
    lon  = np.zeros_like(nc.variables['zeta'][:,:,:])
    lat  = np.zeros_like(nc.variables['zeta'][:,:,:])
    h    = np.zeros_like(nc.variables['zeta'][:,:,:])

    for t in xrange(nt):
        time[t,:,:] = nc.variables['ocean_time'][t]
        h[t,:,:]    = nc.variables['h'][:,:]
    for x in xrange(nx):
        lon[:,:,x] = nc.variables['lon_rho'][0,x]
    for y in xrange(ny):
        lat[:,y,:] = nc.variables['lat_rho'][y,0]
        
    flux['time'] = time.flatten()
    flux['lon']  = lon.flatten()
    flux['lat']  = lat.flatten()
    flux['h']    = h.flatten()

    #

    df = pd.DataFrame(flux)
    num2date = lambda num: netCDF4.num2date(num, tunit)
    df.time  = df.time.apply(num2date)
    df = df.set_index(['time','lon','lat','h'])
    df = df.dropna()

    mean = df.mean()
    mean

    mean.to_csv('{}_mean.csv'.format(csvname))

    df.describe().to_csv('{}_describe.csv'.format(csvname))

    df.sum().to_csv('{}_sum.csv'.format(csvname))

    df.to_csv('{}_all.csv'.format(csvname))

if __name__ == '__main__':

    ncfiles = ['../roms2-1/ob500_avg.nc',
               '../roms2-2/ob500_avg.nc',
               '../roms2-3/ob500_avg.nc',
               '../roms2-4/ob500_avg.nc']

    csvnames = ['avg_2-'+str(i) for i in range(1,5)]

    for ncfile, csvname in zip(ncfiles, csvnames):
        avg2csv(ncfile, csvname)


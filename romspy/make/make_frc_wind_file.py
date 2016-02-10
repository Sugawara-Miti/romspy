# coding: utf-8
# (c) 2015-11-19 Teruhisa Okada

import netCDF4
from numpy import dtype
import datetime
from reshape_wind import reshape_wind
import romspy


def make_frc_wind(frcfile, grdfile, u_out, v_out, t_out):

    td, eta_rho, xi_rho = u_out.shape
    print td, eta_rho, xi_rho
    #print u_out
    #return

    print 'creating', frcfile
    nc = netCDF4.Dataset(frcfile, 'w', format='NETCDF3_CLASSIC') 
    now = datetime.datetime.now()
    nc.history = now.strftime('%Y-%m-%d %H:%M:%S')
    nc.author = 'OKADA Teruhisa'

    print 'creating dimensions'
    nc.createDimension('xi_rho', xi_rho)
    nc.createDimension('eta_rho', eta_rho)
    nc.createDimension('time_wind', None)

    print 'creating variables'
    time = nc.createVariable('time_wind', dtype('double').char, ('time_wind',))
    u = nc.createVariable('Uwind', dtype('float32').char, ('time_wind', 'eta_rho', 'xi_rho'))
    v = nc.createVariable('Vwind', dtype('float32').char, ('time_wind', 'eta_rho', 'xi_rho'))
    time.units = romspy.GMT_days
    u.units = 'meter second-1'
    v.units = 'meter second-1'

    print 'writing variables'
    time[:] = t_out
    u[:,:,:] = u_out
    v[:,:,:] = v_out
    u.time = 'time_wind'
    v.time = 'time_wind'

    nc.close()


if __name__ == '__main__':

    frcfile = 'Z:/Data/ob500_frc_wind_2012_rbf.nc'
    #frcfile = 'ob500_frc_wind_2012_rbf.nc'

    windfiles = ['F:/okada/Data/mp/mp_003_C_20111231_20130101.csv',
                 'F:/okada/Data/mp/mp_005_C_20111231_20130101.csv',
                 'F:/okada/Data/mp/mp_006_C_20111231_20130101.csv',
                 'F:/okada/Data/mp/mp_012_C_20111231_20130101.csv',
                 'F:/okada/Data/jma/jma_akashi_20111231_20130101.csv',
                 'F:/okada/Data/jma/jma_gunge_20111231_20130101.csv',
                 'F:/okada/Data/jma/jma_kansaiAP_20111231_20130101.csv',
                 'F:/okada/Data/jma/jma_kobe_20111231_20130101.csv',
                 'F:/okada/Data/jma/jma_kobeAP_20111231_20130101.csv',
                 'F:/okada/Data/jma/jma_tomogashima_20111231_20130101.csv']

    stafiles = {'mp':'F:/okada/Dropbox/Data/stations13.csv',
                'jma':'F:/okada/Dropbox/Data/stations_jma.csv'}

    grdfile = 'F:/okada/Dropbox/Data/ob500_grd-10.nc'

    u_out, v_out, t_out = reshape_wind(windfiles, stafiles, grdfile, method='rbf_inverse')

    make_frc_wind(frcfile, grdfile, u_out, v_out, t_out)

# coding: utf-8
# (c) 2015-11-18 Teruhisa Okada

import pandas as pd
import numpy as np
import math
from pykrige.ok import OrdinaryKriging
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
import matplotlib as mpl
import netCDF4
import datetime
import romspy

mpl.rc('image', cmap='jet')


def reshape_wind(windfiles, stafiles, grdfile, method='kriging', smooth=1, plot=False):
    u, v = {}, {}
    timedelta = datetime.timedelta(hours=3)
    for windfile in windfiles:
        print windfile
        if 'mp' in windfile:
            names = ['name', 'date', 'direction', 'wind']
            df = pd.read_csv(windfile, encoding='Shift_JIS', names=names, skiprows=1, na_values='*', index_col='date')
            df['u'] = -np.sin(math.pi * df.direction / 180.0) * df.wind
            df['v'] = -np.cos(math.pi * df.direction / 180.0) * df.wind
            df.index = df.index.map(lambda t: datetime.datetime.strptime(t, '%Y/%m/%d %H:%M'))
            df = df.resample('12H', how='mean', loffset=timedelta)
            #df = df.resample('H', how='mean')
            station = int(windfile[-26:-24])
            u[station] = df.u.dropna()
            v[station] = df.v.dropna()
        elif 'jma' in windfile:
            df = pd.read_csv(windfile, encoding='Shift_JIS', na_values='--', index_col='id')
            df['u'] = -np.sin(math.pi * df.wind_direction / 180.0) * df.wind_velocity
            df['v'] = -np.cos(math.pi * df.wind_direction / 180.0) * df.wind_velocity
            df.index = df.index.map(lambda t: datetime.datetime.strptime(t, '%Y/%m/%d %H:%M'))
            df = df.resample('12H', how='mean', loffset=timedelta)
            #df = df.resample('H', how='mean')
            station = windfile[windfile.find('jma_')+4:-22]
            u[station] = df.u.dropna()
            v[station] = df.v.dropna()

    sta_mp = pd.read_csv(stafiles['mp'], index_col='station')
    sta_jma = pd.read_csv(stafiles['jma'], index_col='station')

    grd = netCDF4.Dataset(grdfile, 'r')
    xmesh = grd.variables['lon_rho'][:,:]
    ymesh = grd.variables['lat_rho'][:,:]
    grd.close()

    xgrid = xmesh[0,:]
    ygrid = ymesh[:,0]

    td = len(df)
    xd = len(xgrid)
    yd = len(ygrid)
    u3d = np.zeros(shape=[td, yd, xd])
    v3d = np.zeros_like(u3d)
    time_wind = np.zeros(shape=[td])

    for i, t in enumerate(df.index):
        X, Y, U, V = [], [], [], []
        for station in u.keys():
            try:
                U.append(u[station][t])
                V.append(v[station][t])
                if type(station) == int:
                    X.append(sta_mp.lon[station])
                    Y.append(sta_mp.lat[station])
                elif type(station) == str:
                    X.append(sta_jma.x[station])
                    Y.append(sta_jma.y[station])
            except:
                pass
        print i, t, len(Y)

        if method == 'kriging_gaussian':
            ukrig = OrdinaryKriging(X, Y, U, variogram_model='gaussian', verbose=False, enable_plotting=False)
            vkrig = OrdinaryKriging(X, Y, V, variogram_model='gaussian', verbose=False, enable_plotting=False)
            umesh, ss = ukrig.execute('grid', xgrid, ygrid)
            vmesh, ss = vkrig.execute('grid', xgrid, ygrid)

        elif method == 'kriging_linear':
            ukrig = OrdinaryKriging(X, Y, U, variogram_model='linear', verbose=False, enable_plotting=False)
            vkrig = OrdinaryKriging(X, Y, V, variogram_model='linear', verbose=False, enable_plotting=False)
            umesh, ss = ukrig.execute('grid', xgrid, ygrid)
            vmesh, ss = vkrig.execute('grid', xgrid, ygrid)

        elif method == 'rbf':
            urbf = Rbf(X, Y, U)
            vrbf = Rbf(X, Y, V)
            umesh = urbf(xmesh, ymesh)
            vmesh = vrbf(xmesh, ymesh)

        elif method == 'rbf_gaussian':
            urbf = Rbf(X, Y, U, function='inverse')
            vrbf = Rbf(X, Y, V, function='inverse')
            umesh = urbf(xmesh, ymesh)
            vmesh = vrbf(xmesh, ymesh)

        elif method == 'rbf_linear':
            urbf = Rbf(X, Y, U, function='inverse')
            vrbf = Rbf(X, Y, V, function='inverse')
            umesh = urbf(xmesh, ymesh)
            vmesh = vrbf(xmesh, ymesh)

        elif method == 'rbf_inverse':
            urbf = Rbf(X, Y, U, function='inverse')
            vrbf = Rbf(X, Y, V, function='inverse')
            umesh = urbf(xmesh, ymesh)
            vmesh = vrbf(xmesh, ymesh)

        elif method == 'rbf_inverse_smooth':
            urbf = Rbf(X, Y, U, function='inverse', smooth=smooth)
            vrbf = Rbf(X, Y, V, function='inverse', smooth=smooth)
            umesh = urbf(xmesh, ymesh)
            vmesh = vrbf(xmesh, ymesh)

        if plot == 'pcolor' and i == 0:
            plt.figure(figsize=[15, 5])
            plt.subplot(1,2,1)
            plt.pcolor(xmesh, ymesh, umesh, vmin=-1, vmax=1)
            plt.colorbar()
            plt.subplot(1,2,2)
            plt.pcolor(xmesh, ymesh, vmesh, vmin=-1, vmax=1)
            plt.colorbar()
            plt.show()

        elif plot == 'quiver' and i == 0:
            plt.figure(figsize=[10, 10])
            romspy.basemap('F:/okada/notebook/deg_OsakaBayMap_okada.bln')
            plt.quiver(xmesh[::3, ::3], ymesh[::3, ::3], umesh[::3, ::3], vmesh[::3, ::3], units='width', angles='xy', scale=100)
            plt.quiver(X, Y, U, V, color='r', units='xy', angles='xy', scale=100)
            plt.show()

        u3d[i,:,:] = umesh
        v3d[i,:,:] = vmesh
        time_wind[i] = netCDF4.date2num(t, romspy.JST_days)

    return u3d, v3d, time_wind


if __name__ == '__main__':

    windfiles = ['F:/okada/Dropbox/Data/mp/mp_003_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_005_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_006_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_012_C_20120101_20121231.csv']
    windfiles = ['F:/okada/Dropbox/Data/jma/jma_akashi_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_gunge_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kansaiAP_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kobe_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kobeAP_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kumatori_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_osaka_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_sakai_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_sumoto_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_tomogashima_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_toyonaka_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_wakayama_20120101_20121231.csv']
    windfiles = ['F:/okada/Dropbox/Data/mp/mp_003_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_005_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_006_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_012_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_akashi_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_gunge_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kansaiAP_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kobe_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kobeAP_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kumatori_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_osaka_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_sakai_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_sumoto_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_tomogashima_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_toyonaka_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_wakayama_20120101_20121231.csv']
    windfiles = ['F:/okada/Dropbox/Data/mp/mp_003_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_005_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_006_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/mp/mp_012_C_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_akashi_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_gunge_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kansaiAP_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kobe_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_kobeAP_20120101_20121231.csv',
                 'F:/okada/Dropbox/Data/jma/jma_tomogashima_20120101_20121231.csv']
    stafiles = {'mp':'F:/okada/Dropbox/Data/stations13.csv'}
    stafiles['jma'] = 'F:/okada/Dropbox/Data/stations_jma.csv'
    grdfile = 'F:/okada/Dropbox/Data/ob500_grd-10.nc'

    #reshape_wind(windfiles, stafiles, grdfile, method='kriging_gaussian')
    #reshape_wind(windfiles, stafiles, grdfile, method='kriging_linear')
    #reshape_wind(windfiles, stafiles, grdfile, method='rbf')
    #reshape_wind(windfiles, stafiles, grdfile, method='rbf_gaussian')
    #reshape_wind(windfiles, stafiles, grdfile, method='rbf_linear')
    reshape_wind(windfiles, stafiles, grdfile, method='rbf_inverse', plot='quiver')
    #reshape_wind(windfiles, stafiles, grdfile, method='rbf_inverse_smooth', smooth=0.5)
    #reshape_wind(windfiles, stafiles, grdfile, method='rbf_inverse_smooth', smooth=1)
    #reshape_wind(windfiles, stafiles, grdfile, method='rbf_inverse_smooth', smooth=2)

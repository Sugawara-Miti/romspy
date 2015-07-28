# -*- coding: utf-8 -*-

"""
2014/10/12 okada make this file.
2015/05/01 okada remake it, but test data are no provision.
"""

import datetime
import numpy as np
from numpy import dtype
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
import pandas as pd
import netCDF4


def make_river_file(ncname, metafile, rainfile, yodofile, yamatofile, wqfile):

    s_rho   = 20
    n_river = 34
    tunit_GMT ='days since 1968-05-23 00:00:00 GMT'
    tunit_JST ='days since 1968-05-23 09:00:00 GMT'
    time_out = {}
    meta_out = {}
    hour_out = {}
    annu_out = {}
    dail_out = {}

    print 'read meta'

    meta = pd.read_csv(metafile, index_col='river')
    meta_out['river']           = [i+1 for i in range(n_river)]
    meta_out['river_Xposition'] = meta.xi_rho.tolist()
    meta_out['river_Eposition'] = meta.eta_rho.tolist()
    meta_out['river_direction'] = meta.direction.tolist()
    meta_out['river_flag']      = 3
    meta_out['river_Vshape']    = 0.05

    print 'hourly transport'

    rain = pd.read_csv(rainfile, parse_dates=[['date', 'hour']], index_col='date_hour', na_values='--').fillna(0)
    rain = pd.rolling_mean(rain, window=24).fillna(0)
    q    = pd.DataFrame(rain.precipitation)
    for name in meta.index:
        q[name] = meta.average[name] + q.precipitation/1000.0/3600.0 * meta.area[name]*10**6
        q[name] = q[name] * meta.flag[name]
    del q['precipitation']
    river_names = meta.index
    yodo     = pd.read_csv(yodofile, index_col='time', na_values=0)
    q.yodo1  = -yodo.discharge.interpolate()
    q.yodo2  = -yodo.discharge.interpolate()
    yamato   = pd.read_csv(yamatofile, index_col='time', na_values=0)
    q.yamato = -yamato.discharge.interpolate()
    time = [timestamp.to_datetime() for timestamp in q.index.tolist()]
    time_out['river_time_hourly'] = netCDF4.date2num(time, tunit_JST)

    print time_out['river_time_hourly']

    td_h = len(time_out['river_time_hourly'])
    hour_out['river_transport'] = np.ndarray(shape=[td_h, n_river])
    for i, name in enumerate(river_names):
        hour_out['river_transport'][:,i] = q[name]
    for t in xrange(300):
        hour_out['river_transport'][t,:] = hour_out['river_transport'][t,:] * float(t) / 300.0
    """
    plt.plot(hour_out['river_transport'][:,7])
    plt.show()
    return
    """

    print 'annually salt'

    time = [datetime.datetime(2012,1,1), datetime.datetime(2013,1,1)]
    time_out['river_time_annually'] = netCDF4.date2num(time, tunit_JST)

    print time_out['river_time_annually']

    td_a = len(time_out['river_time_annually'])
    annu_out['river_salt'] = 1.0

    print 'daily temp from Sta.5'

    wq = pd.read_csv(wqfile, parse_dates='time', index_col='time')#.interpolate()
    daily = wq.resample('D', how='mean')
    time = [timestamp.to_datetime() for timestamp in daily.index.tolist()]
    time_out['river_time_daily'] = netCDF4.date2num(time, tunit_JST)

    print time_out['river_time_daily']

    td_d = len(time_out['river_time_daily'])
    dail_out['river_temp'] = np.ndarray(shape=[td_d, s_rho, n_river])
    for t in xrange(td_d):
        dail_out['river_temp'][t,:,:] = daily.temp[t]
    """
    plt.plot(dail_out['river_temp'][:,10,7])
    plt.savefig("river_temp.png")
    return
    """
    """
    print 'daily part: biological tracers by LQ equation'

    csv_lq = 'lq.csv'
    lq = pd.read_csv(csv_lq, index_col=['river', 'name'])
    a = lq.a
    b = lq.b
    cff = 1000000.0 / 86400.0
    yodo_names   = a['yodo'  ].index
    yamato_names = a['yamato'].index
    yodo   = {}
    yamato = {}
    for name in yodo_names:
        yodo[name] = a['yodo'][name] * ( (np.abs(q['yodo1'])*2+(70+10+40))**(b['yodo'][name]-1)) * cff
    for name in yamato_names:
        yamato[name] = a['yamato'][name] * (np.abs(q['yamato'])**(b['yamato'][name]-1)) * cff
    for name in ['TN', 'TDN', 'NH4-N', 'NO2-N', 'NO3-N', 'DIN', 'DON', 'PN']:
        yodo[name]   = yodo[name]   / 14 * 1000
        yamato[name] = yamato[name] / 14 * 1000
    for name in ['TP', 'TDP', 'PO4-P', 'DOP', 'PP']:
        yodo[name]   = yodo[name]   / 31 * 1000
        yamato[name] = yamato[name] / 31 * 1000
    for name in ['TOC', 'DOC', 'POC']:
        yamato[name] = yamato[name] / 12 * 1000
        yodo[name]   = yamato[name]
    yodo['NO23-N']   = yodo['NO2-N']   + yodo['NO3-N']
    yamato['NO23-N'] = yamato['NO2-N'] + yamato['NO3-N']
    yodo   = pd.DataFrame(yodo  ).interpolate().resample('D', how='mean')
    yamato = pd.DataFrame(yamato).interpolate().resample('D', how='mean')
    mean = {}
    for name in yodo.columns:
        mean[name] = [ ( yodo[name].mean() + yamato[name].mean())/2 for _ in xrange(367) ]
    mean = pd.DataFrame(mean)

    data = ['NH4', 'NO3', 'SDeN', 'LDeN', 'PO4', 'SDeP', 'LDeP', 'SDeC', 'LDeC']
    for name in data:
        dail_out['river_'+name] = np.ndarray(shape=[td_d, s_rho, n_river])
    var = {}
    for name in river_names:
        if   name == 'yodo1':  var[name] = yodo
        elif name == 'yodo2':  var[name] = yodo
        elif name == 'yamato': var[name] = yamato
        else:                  var[name] = mean
    for i, name in enumerate(river_names):
        for s in xrange(s_rho):
            dail_out['river_NH4'] [:,s,i] = var[name]['NH4-N']
            dail_out['river_NO3'] [:,s,i] = var[name]['NO23-N']
            dail_out['river_SDeN'][:,s,i] = var[name]['DON']
            dail_out['river_LDeN'][:,s,i] = var[name]['PN']
            dail_out['river_PO4'] [:,s,i] = var[name]['PO4-P']
            dail_out['river_SDeP'][:,s,i] = var[name]['DOP']
            dail_out['river_LDeP'][:,s,i] = var[name]['PP']
            dail_out['river_SDeC'][:,s,i] = var[name]['DOC']
            dail_out['river_LDeC'][:,s,i] = var[name]['POC']
    dail_names = dail_out.keys()
    """

    print 'annually biology'

    data = ['NH4', 'NO3', 'SDeN', 'Oxyg', 'PO4', 'SDeP']
    for name in data:
        annu_out['river_'+name] = np.ndarray(shape=[td_a, s_rho, n_river])
    for i, name in enumerate(river_names):
        if name == 'yodo1' or name == 'yodo2':
            annu_out['river_NH4'][:,:,i]  = 8.10
            annu_out['river_NO3'][:,:,i]  = 41.4
            annu_out['river_SDeN'][:,:,i] = 28.0*10.0/34.0
            annu_out['river_PO4'][:,:,i]  = 3.07
            annu_out['river_SDeP'][:,:,i] = 1.4*38.0/63.0
        elif name == 'yamato':
            annu_out['river_NH4'][:,:,i]  = 9.0
            annu_out['river_NO3'][:,:,i]  = 214.8
            annu_out['river_SDeN'][:,:,i] = 28.0*10.0/34.0
            annu_out['river_PO4'][:,:,i]  = 12.07
            annu_out['river_SDeP'][:,:,i] = 2.7*38.0/63.0
        else:
            annu_out['river_NH4'][:,:,i]  = 8.5
            annu_out['river_NO3'][:,:,i]  = 105.7
            annu_out['river_SDeN'][:,:,i] = 28.0*10.0/34.0
            annu_out['river_PO4'][:,:,i]  = 6.1
            annu_out['river_SDeP'][:,:,i] = 2.0*38.0/63.0
    annu_out['river_Oxyg'][:,:,:] = 312.5
    """
    dail_out['river_chlorophyll']   = np.ndarray(shape=[td_d, s_rho, n_river])
    dail_out['river_phytoplankton'] = np.ndarray(shape=[td_d, s_rho, n_river])
    dail_out['river_zooplankton']   = np.ndarray(shape=[td_d, s_rho, n_river])
    Chl2C = 0.05   # okada (=1/20 gChl/gC)
    PhyCN = 6.625  # (=106/16 molC/molN)
    for t in xrange(td_d):
        dail_out['river_chlorophyll'][t,:,:]   = daily.chlorophyll[t]
        dail_out['river_phytoplankton'][t,:,:] = daily.chlorophyll[t] / Chl2C / 12.0 / PhyCN
        dail_out['river_zooplankton'][t,:,:]   = daily.chlorophyll[t] * 0.1
        """

    meta_names = meta_out.keys()
    annu_names = annu_out.keys()
    dail_names = dail_out.keys()

    print 'writing part'

    nc = netCDF4.Dataset(ncname, 'w', format='NETCDF3_CLASSIC')
    nc.createDimension('s_rho', s_rho)
    nc.createDimension('river', n_river)
    nc.createDimension('time_annually', td_a)
    nc.createDimension('time_daily',    td_d)
    nc.createDimension('time_hourly',   td_h)
    time_a = nc.createVariable('river_time_annually', dtype('double').char, ('time_annually',))
    time_d = nc.createVariable('river_time_daily',    dtype('double').char, ('time_daily',))
    time_h = nc.createVariable('river_time_hourly',   dtype('double').char, ('time_hourly',))
    trans  = nc.createVariable('river_transport',dtype('float32').char, ('time_hourly','river'))
    meta = {}
    annu = {}
    dail = {}
    for name in meta_names:
        if name == 'river_Vshape':
            meta[name] = nc.createVariable(name,dtype('float32').char,('s_rho','river'))
        else:
            meta[name] = nc.createVariable(name,dtype('float32').char,('river',))
    for name in annu_names:
        annu[name] = nc.createVariable(name,dtype('float32').char,('time_annually','s_rho','river'))
    for name in dail_names:
        dail[name] = nc.createVariable(name,dtype('float32').char,('time_daily','s_rho','river'))
    time_a.units = tunit_GMT
    time_d.units = tunit_GMT
    time_h.units = tunit_GMT
    trans.units  = "meter3 second-1"
    annu['river_salt'].units = "PSU"
    dail['river_temp'].units = "Celius"
    annu['river_NO3'].units  = "millimole_nitrogen meter-3"
    annu['river_NH4'].units  = "millimole_nitrogen meter-3"
    annu['river_SDeN'].units = "millimole_nitrogen meter-3"
    annu['river_Oxyg'].units = "millimole_oxygen meter-3"
    annu['river_PO4'].units  = "millimole_phosphorus meter-3"
    annu['river_SDeP'].units = "millimole_phosphorus meter-3"
    for name in meta_names:
        meta[name].units = 'nondimensional'
    time_a[:]  = time_out['river_time_annually']
    time_d[:]  = time_out['river_time_daily']
    time_h[:]  = time_out['river_time_hourly']
    trans[:,:] = hour_out['river_transport']
    for name in meta_names:
        print name
        if name == 'river_Vshape':
            meta[name][:,:] = meta_out[name]
        else:
            meta[name][:] = meta_out[name]
    for name in annu_names:
        print name
        annu[name][:,:,:] = annu_out[name]
    for name in dail_names:
        print name
        dail[name][:,:,:] = dail_out[name]
    trans.time = 'river_time_hourly'
    for name in annu_names:
        annu[name].time = 'river_time_annually'
    for name in dail_names:
        dail[name].time = 'river_time_daily'
    nc.close()


if __name__ == '__main__':

    ncname = '/Users/teruhisa/Dropbox/Data/ob500_river_2012_fennelP-2.nc'
    metafile = '/Users/teruhisa/Dropbox/Data/river/meta34.csv'
    rainfile = '/Users/teruhisa/Dropbox/Data/river/rain_2012.csv'
    yodofile = '/Users/teruhisa/Dropbox/Data/river/yodo_2012.csv'
    yamatofile = '/Users/teruhisa/Dropbox/Data/river/yamato_2012.csv'
    wqfile = '/Users/teruhisa/Dropbox/Data/river/wq_2012.csv'

    make_river_file(ncname, metafile, rainfile, yodofile, yamatofile, wqfile)

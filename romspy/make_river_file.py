# -*- coding: utf-8 -*-

"""
2014/10/12 okada make this file.
2015/05/01 okada remake it, but test data are no provision.
"""

import datetime
import numpy as np
from numpy import dtype
import pandas as pd
import netCDF4
import romspy


def read_meta(metafile, d):
    print 'read meta'
    meta = pd.read_csv(metafile, index_col='river')
    meta_out = {}
    meta_out['river']           = [i+1 for i in range(d['n_river'])]
    meta_out['river_Xposition'] = meta.xi_rho.tolist()
    meta_out['river_Eposition'] = meta.eta_rho.tolist()
    meta_out['river_direction'] = meta.direction.tolist()
    meta_out['river_flag']      = 3
    meta_out['river_Vshape']    = [float(s) / d['s_rho'] / 10 for s in range(d['s_rho'])]
    return meta_out, meta


def read_trans(rainfile, yodofile, yamatofile, meta, d):
    print 'hourly transport'
    print 'rain:', rainfile
    print 'yodo:', yodofile
    print 'yamato:', yamatofile
    rain = pd.read_csv(rainfile, parse_dates={'time':['date', 'hour']}, index_col='time', na_values='--').fillna(0)
    rain = pd.rolling_mean(rain, window=24, center=False).fillna(0)
    q    = pd.DataFrame(rain.precipitation)
    for name in meta.index:
        q[name] = meta.average[name] + q.precipitation/1000.0/3600.0 * meta.area[name]*10**6
        q[name] = q[name] * meta.flag[name]
    del q['precipitation']
    yodo     = pd.read_csv(yodofile, index_col='time', na_values=0)
    q.yodo1  = -yodo.discharge.interpolate().values
    q.yodo2  = -yodo.discharge.interpolate().values
    yamato   = pd.read_csv(yamatofile, index_col='time', na_values=0)
    q.yamato = -yamato.discharge.interpolate().values
    time = [timestamp.to_datetime() for timestamp in q.index.tolist()]
    print q.head()

    time_out = {}
    time_out['river_time_hourly'] = netCDF4.date2num(time, romspy.JST_days)
    print time_out['river_time_hourly']

    td_h = len(time_out['river_time_hourly'])
    hour_out = {}
    hour_out['river_transport'] = np.ndarray(shape=[td_h, d['n_river']])
    river_names = meta.index
    for i, name in enumerate(river_names):
        hour_out['river_transport'][:,i] = q[name]
    for t in xrange(744):
        hour_out['river_transport'][t,:] = hour_out['river_transport'][t,:] * float(t) / 744.0
    return hour_out, time_out


def set_annually(time_out):
    print 'annually salt'
    time = [datetime.datetime(2012,1,1), datetime.datetime(2013,1,1)]
    time_out['river_time_annually'] = netCDF4.date2num(time, romspy.JST_days)
    print time_out['river_time_annually']
    annu_out = {}
    annu_out['river_salt'] = 1.0
    return annu_out, time_out


def read_daily(wqfile, time_out, d):
    print 'daily temp from Sta.5'
    #wq = pd.read_csv(wqfile, parse_dates='time', index_col='time').interpolate()
    wq = pd.read_csv(wqfile, parse_dates='time', index_col='time')
    daily = wq.resample('D', how='mean')
    time = [timestamp.to_datetime() for timestamp in daily.index.tolist()]
    time_out['river_time_daily'] = netCDF4.date2num(time, romspy.JST_days)
    print time_out['river_time_daily']
    td_d = len(time_out['river_time_daily'])
    dail_out = {}
    dail_out['river_temp'] = np.ndarray(shape=[td_d, d['s_rho'], d['n_river']])
    for t in xrange(td_d):
        dail_out['river_temp'][t,:,:] = daily.temp[t]
    return dail_out, time_out


def set_biology_lq(csv_lq, dail_out, time_out, q, meta, d):
    print 'daily part: biological tracers by LQ equation'
    lq = pd.read_csv(csv_lq, index_col=['river', 'name'])
    a = lq.a
    b = lq.b
    cff = 1000000.0 / 86400.0
    yodo_names   = a['yodo'].index
    yamato_names = a['yamato'].index
    yodo   = {}
    yamato = {}
    for name in yodo_names:
        yodo[name] = a['yodo'][name] * ((np.abs(q['yodo1'])*2+(70+10+40))**(b['yodo'][name]-1)) * cff
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
    yodo   = pd.DataFrame(yodo).interpolate().resample('D', how='mean')
    yamato = pd.DataFrame(yamato).interpolate().resample('D', how='mean')
    mean = {}
    for name in yodo.columns:
        mean[name] = [(yodo[name].mean() + yamato[name].mean())/2 for _ in xrange(367)]
    mean = pd.DataFrame(mean)

    data = ['NH4', 'NO3', 'SDeN', 'LDeN', 'PO4', 'SDeP', 'LDeP', 'SDeC', 'LDeC']
    td_d = len(time_out['river_time_daily'])
    for name in data:
        dail_out['river_'+name] = np.ndarray(shape=[td_d, d['s_rho'], d['n_river']])
    var = {}
    river_names = meta.index
    for name in river_names:
        if name == 'yodo1':
            var[name] = yodo
        elif name == 'yodo2': 
            var[name] = yodo
        elif name == 'yamato':
            var[name] = yamato
        else:
            var[name] = mean
    for i, name in enumerate(river_names):
        for s in xrange(d['s_rho']):
            dail_out['river_NH4'][:,s,i]  = var[name]['NH4-N']
            dail_out['river_NO3'][:,s,i]  = var[name]['NO23-N']
            dail_out['river_SDeN'][:,s,i] = var[name]['DON']
            dail_out['river_LDeN'][:,s,i] = var[name]['PN']
            dail_out['river_PO4'][:,s,i]  = var[name]['PO4-P']
            dail_out['river_SDeP'][:,s,i] = var[name]['DOP']
            dail_out['river_LDeP'][:,s,i] = var[name]['PP']
            dail_out['river_SDeC'][:,s,i] = var[name]['DOC']
            dail_out['river_LDeC'][:,s,i] = var[name]['POC']
    return dail_out


def set_biology(annu_out, time_out, meta, d):
    print 'annually biology'
    data = ['NH4', 'NO3', 'SDeN', 'Oxyg', 'PO4', 'SDeP']
    td = len(time_out['river_time_annually'])
    for name in data:
        annu_out['river_'+name] = np.ndarray(shape=[td, d['s_rho'], d['n_river']])
    river_names = meta.index
    for i, name in enumerate(river_names):
        if name == 'yodo1' or name == 'yodo2':
            annu_out['river_NH4'][:,:,i]  = 0.04 * romspy.g2mol_N  # 0.5
            annu_out['river_NO3'][:,:,i]  = 0.85 * romspy.g2mol_N  # 1.0
            annu_out['river_SDeN'][:,:,i] = 0.21 * romspy.g2mol_N  # 1.0
            annu_out['river_PO4'][:,:,i]  = 0.050 * romspy.g2mol_P  # 0.1
            annu_out['river_SDeP'][:,:,i] = 0.029 * romspy.g2mol_P  # 0.1
        elif name == 'yamato':
            annu_out['river_NH4'][:,:,i]  = 0.11 * romspy.g2mol_N  # 0.5
            annu_out['river_NO3'][:,:,i]  = 3.02 * romspy.g2mol_N  # 2.0
            annu_out['river_SDeN'][:,:,i] = 0.67 * romspy.g2mol_N  # 1.0
            annu_out['river_PO4'][:,:,i]  = 0.297 * romspy.g2mol_P  # 0.4
            annu_out['river_SDeP'][:,:,i] = 0.067 * romspy.g2mol_P  # 0.4
        else:
            annu_out['river_NH4'][:,:,i]  = 0.08 * romspy.g2mol_N  # 0.5
            annu_out['river_NO3'][:,:,i]  = 1.94 * romspy.g2mol_N  # 1.5
            annu_out['river_SDeN'][:,:,i] = 0.44 * romspy.g2mol_N  # 1.0
            annu_out['river_PO4'][:,:,i]  = 0.173 * romspy.g2mol_P  # 0.2
            annu_out['river_SDeP'][:,:,i] = 0.048 * romspy.g2mol_P  # 0.2
    annu_out['river_Oxyg'][:,:,:] = 9.6 * romspy.g2mol_O2  # 8.0
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
    return annu_out


def write_nc(ncname, meta_out, time_out, hour_out, annu_out, dail_out, d):
    print 'writing part'
    meta_names = meta_out.keys()
    annu_names = annu_out.keys()
    dail_names = dail_out.keys()

    nc = netCDF4.Dataset(ncname, 'w', format='NETCDF3_CLASSIC')
    nc.createDimension('s_rho', d['s_rho'])
    nc.createDimension('river', d['n_river'])
    nc.createDimension('time_annually', len(time_out['river_time_annually']))
    nc.createDimension('time_daily',    len(time_out['river_time_daily']))
    nc.createDimension('time_hourly',   len(time_out['river_time_hourly']))
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
    time_a.units = romspy.GMT_days
    time_d.units = romspy.GMT_days
    time_h.units = romspy.GMT_days
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
            for n in range(d['n_river']):
                meta[name][:,n] = meta_out[name]
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


def make_river_file(ncname, metafile, rainfile, yodofile, yamatofile, wqfile):

    d = {'s_rho':20, 'n_river':34}
    meta_out, meta = read_meta(metafile, d)
    hour_out, time_out = read_trans(rainfile, yodofile, yamatofile, meta, d)
    annu_out, time_out = set_annually(time_out)
    dail_out, time_out = read_daily(wqfile, time_out, d)
    annu_out = set_biology(annu_out, time_out, meta, d)

    write_nc(ncname, meta_out, time_out, hour_out, annu_out, dail_out, d)


if __name__ == '__main__':

    #HOME = 'F:/okada'
    HOME = '/home/okada'
    ncname = HOME+'/Dropbox/Data/ob500_river_2012_P-6.nc'
    #metafile = HOME+'/Dropbox/Data/river/meta34.csv'
    metafile = HOME+'/Dropbox/Data/river/meta34_2.csv'  # P-5
    rainfile = HOME+'/Dropbox/Data/river/rain_2012.csv'
    #yodofile = HOME+'/Dropbox/Data/river/yodo_2012.csv'
    yodofile = HOME+'/Dropbox/Data/river/yodo_2012_dynamicwave.csv'  # P-6
    yamatofile = HOME+'/Dropbox/Data/river/yamato_2012.csv'
    tempfile = HOME+'/Dropbox/Data/river/wq_2012.csv'

    make_river_file(ncname, metafile, rainfile, yodofile, yamatofile, tempfile)

# coding: utf-8
# (c) 2015 Teruhisa Okada

import pandas as pd
import romspy


def _read(obsfiles):
    for station, obsfile in obsfiles.items():
        print station, obsfile
        if station in [8,9]:
            names = ['station', 'date', 'layer', 'depth', 'bottom', 'temp']
        if station in [1,2,10,11]:
            names = ['station', 'date', 'layer', 'depth', 'bottom', 'temp', 'salt']
        else:
            names = ['station', 'date', 'layer', 'depth', 'bottom', 'temp', 'salt', 
                      'light', 'DOp', 'FTU', 'chlorophyllf']
        df = pd.read_csv(obsfile, names=names, skiprows=1, parse_dates=['date'], index_col='date', na_values='*') 
        df.station = station
        try:
            df2 = pd.concat([df2, df], axis=0)
        except:
            df2 = df
    return df2


def _convert_depth(df, tidefile):
    print '_convert_depth'
    df = _add_tide(df, tidefile)
    for station in [5, 8, 9]:
        df.loc[df.station==station, 'depth'] += 74.9 * 0.01                                    # CDL -> TP 
        df.loc[df.station==station, 'depth'] += df.loc[df.station==station, 'tide_tp'] * 0.01  # TP -> surface
    return df


def _add_tide(df, tidefile):
    print '_add_tide'
    df2 = pd.read_csv(tidefile, parse_dates='date', index_col='date')  # , date_parser=romspy.date_parser
    df['tide_tp'] = df2.tide_tp
    df['tide_op'] = df2.tide_op
    return df


def _convert_bio(df, chlo_f2g=None):
    print '_convert_bio',
    if chlo_f2g is None:
        chlo_f2g = 1.92  # 2015-11-24
    print 'chlo_f2g =',chlo_f2g
    if 'chlorophyllf' in df.columns:
        print ' chlorophyllf => chlorophyllg'
        df['chlorophyllg'] = df.chlorophyllf * chlo_f2g
    if 'DOp' in df.columns:
        print ' DOp => DOmol'
        df['DOmol'] = romspy.DOp2mol(df.DOp, df.temp, df.salt)
    return df


def _reshape(df):
    print '_reshape',
    vtypes = {}
    if 'temp' in df.columns:
        vtypes['temp'] = 6
    if 'salt' in df.columns:
        vtypes['salt'] = 7
    if 'chlorophyllg' in df.columns:
        vtypes['chlorophyllg'] = 10
    if 'DOmol' in df.columns:
        vtypes['DOmol'] = 15
    print vtypes
    columns = ['station','layer','depth','value']
    for vname, vtype in vtypes.items():
        var = df[['station','layer','depth',vname]]
        var = var.dropna()
        var.columns = columns
        var['type'] = vtype
        try:
            df2 = df2.append(var)
        except:
            df2 = var
    return df2


if __name__ == '__main__':
    """
    obsfile_tmp = 'F:/okada/Data/mp/mp_{0:03}_A_20111231_20130101.csv'
    tidefile    = 'F:/okada/Data/tide/tide_OS_2012.csv'
    outfile     = 'F:/okada/Data/mp/converted_mp.csv'
    """
    obsfile_tmp = '/home/okada/Data/mp/mp_{0:03}_A_20111231_20130101.csv'
    tidefile    = '/home/okada/Data/tide/tide_OS_2012.csv'
    outfile     = '/home/okada/Data/mp/converted_mp-2.csv'

    obsfiles = {i:obsfile_tmp.format(i) for i in range(1,14)}
    #obsfiles = {i:obsfile_tmp.format(i) for i in [1]}

    df = _read(obsfiles)
    df = _convert_bio(df)
    df = _convert_depth(df, tidefile)
    df = _reshape(df)
    df.to_csv(outfile)

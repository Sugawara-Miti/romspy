# coding: utf-8
# (c) 2015-12-09 Teruhisa Okada

import pandas as pd
import matplotlib.pyplot as plt
import romspy


def _read_mp(csvfile):
    print csvfile
    df = pd.read_csv(csvfile, encoding='Shift_JIS', parse_dates=u'観測日時', na_values='*')
    return df


def _rename(df):
    if len(df.columns) == 11:
        names = ['station', 'date', 'layer', 'depth', 'bottom', 'temp', 'salt', 'light', 'DOp', 'FTU', 'chlo']
    if len(df.columns) == 7:
        names = ['station', 'date', 'layer', 'depth', 'bottom', 'temp', 'salt']
    if len(df.columns) == 6:
        names = ['station', 'date', 'layer', 'depth', 'bottom', 'temp']
    df.columns = names
    return df


def parse_mp(tmpfile, station):
    csvfile = tmpfile.format(station)
    df = _read_mp(csvfile)
    df = _rename(df)
    df.station = station
    return df


def pickup(tmpfile, station, **kw):
    df = parse_mp(tmpfile, station)
    #sta = df[df.station==station]
    if 'layer' in kw.keys():
        layer = kw.pop("layer")
        df = df[df.layer==layer]
    if 'dates' in kw.keys():
        dates = kw.pop("dates")
        df = df[(df.date>=dates[0]) & (df.date<dates[-1])]
    return df


def _test_read_mp(tmpfile):
    dfa = parse_mp(tmpfile, 3)
    for s in [1,2,4,5,6,7,8,9,10,11,12,13]:
        df = parse_mp(tmpfile, s)
        dfa = dfa.append(df)
    print dfa.head()


def _test_pickup(tmpfile):
    station = 1
    layer = 1.0
    df = pickup(tmpfile, station, layer)
    print df.head()


def _test_pickup2(tmpfile):
    dates = ["2012/08/01 00:00", "2012/08/08 00:00"]
    #dates = [datetime.datetime(2012,8,1,0), datetime.datetime(2012,9,1,0)]
    df = pickup(tmpfile, station=4, layer=1.0, dates=dates)
    df.index = pd.to_datetime(df.date, '%Y/%m/%d %H:%M')
    plt.plot(df.index.values, df.light.values, '-')
    plt.show()


if __name__ == '__main__':
    import datetime

    #tmpfile = 'F:/okada/Data/mp/mp_{0:03d}_A_20111231_20130101.csv'
    #_test_(tmpfile)
    #_test_pickup2(tmpfile)

    csvfile = 'F:/okada/Data/mp/mp_004_B_20111231_20130101.csv'
    #_test_(tmpfile)
    df = _read_mp(csvfile)
    print df.head()
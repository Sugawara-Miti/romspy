# coding: utf-8
# (c) 2015-12-09 Teruhisa Okada

import pandas as pd


def _read_mp(csvfile):
    print csvfile
    df = pd.read_csv(csvfile, parse_dates=1, na_values='*', index_col=1)
    return df


def _rename(df):
    if len(df.columns) == 10:
        names = ['station', 'layer', 'depth', 'bottom', 'temp', 'salt', 'light', 'DOp', 'FTU', 'chlo']
    if len(df.columns) == 6:
        names = ['station', 'layer', 'depth', 'bottom', 'temp', 'salt']
    if len(df.columns) == 5:
        names = ['station', 'layer', 'depth', 'bottom', 'temp']
    df.columns = names
    df.index.name = 'date'
    return df


def _restation(df):
    s = {}
    s[u'明石海峡航路東方灯浮標'] = 1
    s[u'洲本沖灯浮標'] = 2
    s[u'関空ＭＴ局'] = 3
    s[u'神戸港波浪観測塔'] = 4
    s[u'淀川河口'] = 5
    s[u'阪南沖窪地'] = 6
    s[u'堺浜'] = 7
    s[u'神戸六甲アイランド東水路中央第三号灯標'] = 8
    s[u'浜寺航路第十号灯標'] = 9
    s[u'淡路交流の翼港'] = 10
    s[u'須磨海づり公園'] = 11
    s[u'大阪港波浪観測塔'] = 12
    s[u'岸和田沖'] = 13
    resta = lambda station: s[station.decode('Shift_JIS')]
    df.station = df.station.apply(resta)
    return df


def read_mp(csvfile):
    df = _read_mp(csvfile)
    df = _rename(df)
    df = _restation(df)
    return df


if __name__ == '__main__':
    csvfile = 'F:/okada/Data/mp/mp_001_A_20111231_20130101.csv'
    df = read_mp(csvfile)
    print df


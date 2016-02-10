# coding: utf-8
# (c) 2015-11-10 Teruhisa Okada

import pandas as pd
import datetime


def tide_parser(hryfile=None):

    #time_string = hryfile[-12:-6]
    f = open(hryfile)

    def row2dt(row):
        year = row[72:74]
        month = row[74:76]
        day = row[76:78]
        dt_start = datetime.datetime(int('20'+year), int(month), int(day))
        return [dt_start + datetime.timedelta(hours=i) for i in range(24)]

    dates = []
    tides = []
    for row in f.readlines():
        date = row2dt(row)
        dates.extend(date)
        tide = [row[3*i:3*i+3] for i in range(24)]
        tides.extend(tide)

    df = pd.DataFrame({'date':dates, 'tide':tides})
    str2int = lambda tide: None if tide == '   ' else int(tide)
    df.tide = df.tide.apply(str2int)
    return df


def line_parser(linefile, mode='line'):
    df = pd.read_csv(linefile)
    if mode == 'df':
        return df
    else:
        return [[df.x[i], df.y[i]] for i in df.index]


def date_parser(date):
    try:
        return datetime.datetime.strptime(date, '%Y/%m/%d %H:%M')
    except:
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':

    hryfile = 'F:/okada/Data/tide/hry201209OS.txt'
    print tide_parser(hryfile)

    linefile = 'F:/okada/Dropbox/Data/stations_abcd_osaka-bay.csv'
    #print line_parser(linefile)

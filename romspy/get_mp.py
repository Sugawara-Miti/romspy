# coding: utf-8
# (c) 2015-11-18 Teruhisa Okada

import urllib
import datetime
import pandas as pd
import csv
import shutil


def get_mp(outdir, year=2012, stations=None, items=['A','B','C']):

    url_tmp = 'http://222.158.204.199/obweb/data/c1/c1_csv_output.aspx?dataid={0:03d}&soutitypeid={1}&from={2}&to={3}'
    outfile_tmp = outdir + 'mp_{0:03d}_{1}_{2}_{3}.csv'

    if stations is None:
        stations = [i+1 for i in range(13)]

    #d_start = datetime.datetime(year, 1, 1, 0)
    #d_end = datetime.datetime(year, 12, 31, 0)
    d_start = datetime.date(year-1, 12, 31)
    d_end = datetime.date(year+1, 1, 1)
    s_start = d_start.strftime('%Y%m%d')
    s_end = d_end.strftime('%Y%m%d')

    for station in stations:
        print 'downloading mp sta.{}'.format(station)
        for item in items:
            url = url_tmp.format(station, item, s_start, s_end)
            outfile = outfile_tmp.format(station, item, s_start, s_end)
            urllib.urlretrieve(url, outfile)


def correct_mp(outfile, n_columns=6):
    print outfile,
    try:
        df = pd.read_csv(outfile)
        print len(df)
    except:
        shutil.copyfile(outfile, outfile+'-old.csv')
        rows = []
        with open(outfile, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == n_columns:
                    rows.append(row)
                else:
                    print len(row), row[-6:]
                    rows.append(row[-6:])
        with open(outfile, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(rows)


if __name__ == '__main__':

    #get_mp('F:/okada/Data/mp/', year=2012, items=['A', 'B'])

    correct_mp('F:/okada/Data/mp/mp_009_A_20111231_20130101.csv', n_columns=6)

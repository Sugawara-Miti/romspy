# coding: utf-8
# (c) 2015-11-18 Teruhisa Okada

import urllib
import datetime


def get_rader(outdir, year, dataid):

    #url_tmp = 'http://222.158.204.199/obweb/data/c1/c1_csv_output.aspx?dataid={0:03d}&soutitypeid={1}&from={2}&to={3}'
    #url_tmp = 'http://222.158.204.199/obweb/data/c1/c1_csv_output.aspx?dataid={0:03d}&soutitypeid=F&id=1&from={1}&to={2}'
    #url_tmp = 'http://222.158.204.199/obweb/data/c1/c1_csv_output.aspx?from={}&to={}'
    url_tmp = 'http://222.158.204.199/obweb/data/C5/c5_output3.aspx?dataid=000&soutitypeid=A&from={1}&to={2}'
    outfile_tmp = outdir + 'rader_{}_{}_{}.csv'

    print 'downloading rader data'
    #d_start = datetime.datetime(year, 1, 1, 0)
    #d_end = datetime.datetime(year, 12, 31, 0)
    d_start = datetime.date(year-1, 12, 31)
    d_end = datetime.date(year+1, 1, 1)
    s_start = d_start.strftime('%Y%m%d')
    s_end = d_end.strftime('%Y%m%d')

    url = url_tmp.format(dataid, s_start, s_end)
    print url
    outfile = outfile_tmp.format(dataid, s_start, s_end)
    print outfile
    urllib.urlretrieve(url, outfile)


if __name__ == '__main__':

    for i in range(20):
        get_rader('F:/okada/Data/rader/', year=2012, dataid=i)

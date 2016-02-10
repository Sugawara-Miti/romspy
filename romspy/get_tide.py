# coding: utf-8
# (c) 2015-11-18 Teruhisa Okada

import urllib
import romspy


def get_tide(outdir, year=2012, station='OS'):

    #url_tmp = 'http://222.158.204.199/obweb/data/c1/c1_csv_output.aspx?dataid={0:03d}&soutitypeid={1}&from={2}&to={3}'
    url_tmp = 'http://www.data.jma.go.jp/gmd/kaiyou/data/db/tide/genbo/{0}/{0}{1:02d}/hry{0}{1:02d}{2}.txt'
    outfile_tmp = outdir + 'hry{0}{1:02d}{2}.txt'

    print 'downloading tide {}'.format(station)
    #d_start = datetime.date(year-1, 12, 31)
    #d_end = datetime.date(year+1, 1, 1)
    #s_start = d_start.strftime('%Y%m%d')
    #s_end = d_end.strftime('%Y%m%d')
    for month in range(1,13):
        url = url_tmp.format(year, month, station)
        outfile = outfile_tmp.format(year, month, station)
        print outfile
        urllib.urlretrieve(url, outfile)

        df = romspy.tide_parser(outfile)
        try:
            df2 = df2.append(df)
        except:
            df2 = df
    if station == 'OS':
        df2['tide_tp'] = df2.tide - 353.7
    df2['tide_op'] = df2.tide_tp + 120.0
    return df2


if __name__ == '__main__':

    df2 = get_tide('F:/okada/Data/tide/', year=2012)
    df2.to_csv('F:/okada/Data/tide/tide_OS_2012.csv', index=None)
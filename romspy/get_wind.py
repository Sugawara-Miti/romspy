# coding: utf-8
# (c) 2015-11-18 Teruhisa Okada

import urllib
import urllib2
import datetime
from bs4 import BeautifulSoup
import re


def get_mp_wind(outdir, year=2012, stations=None, items=['A','B','C']):

    url_tmp = 'http://222.158.204.199/obweb/data/c1/c1_csv_output.aspx?dataid={0:03d}&soutitypeid={1}&from={2}&to={3}'
    outfile_tmp = outdir + 'mp_{0:03d}_{1}_{2}_{3}.csv'

    if stations is None:
        stations = [i+1 for i in range(13)]

    for station in stations:
        print 'downloading mp sta.{}'.format(station)
        #d_start = datetime.datetime(year, 1, 1, 0)
        #d_end = datetime.datetime(year, 12, 31, 0)
        d_start = datetime.date(year-1, 12, 31)
        d_end = datetime.date(year+1, 1, 1)
        s_start = d_start.strftime('%Y%m%d')
        s_end = d_end.strftime('%Y%m%d')
        for item in items:
            url = url_tmp.format(station, item, s_start, s_end)
            outfile = outfile_tmp.format(station, item, s_start, s_end)
            urllib.urlretrieve(url, outfile)


def get_jma_wind(outdir, year=2012, stations=None):

    outfile = outdir + 'jma_{}_{}_{}.csv'

    url = {}
    url_tmp = 'http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_{}.php?prec_no={}&block_no={}&year=%d&month=%d&day=%d&view='
    url['osaka'] = url_tmp.format('s1', 62, 47772)
    #url['hirakata'] = url_tmp.format('a1', 62, 1065)
    url['sakai'] = url_tmp.format('a1', 62, 1062)
    url['toyonaka'] = url_tmp.format('a1', 62, '0602')
    url['kumatori'] = url_tmp.format('a1', 62, '0606')
    url['kansaiAP'] = url_tmp.format('a1', 62, 1471)

    url['kobe'] = url_tmp.format('s1', 63, 47770)
    url['kobeAP'] = url_tmp.format('a1', 63, 1587)
    url['gunge'] = url_tmp.format('a1', 63, '0970')
    #url['awaji'] = url_tmp.format('a1', 63, 1448)
    #url['nishimoniya'] = url_tmp.format('a1', 63, 1588)
    url['sumoto'] = url_tmp.format('s1', 63, 47776)
    url['akashi'] = url_tmp.format('a1', 63, '0625')

    url['wakayama'] = url_tmp.format('s1', 65, 47777)
    url['tomogashima'] = url_tmp.format('a1', 65, 1457)

    #d_start = datetime.date(year, 1, 1)
    #d_end = datetime.date(year, 12, 31)
    d_start = datetime.date(year-1, 12, 31)
    d_end = datetime.date(year+1, 1, 1)
    s_start = d_start.strftime('%Y%m%d')
    s_end = d_end.strftime('%Y%m%d')
    dates = [d_start + datetime.timedelta(days=t) for t in range(368)]

    for sname in url.keys():
        print 'downloading jma {}'.format(sname)
        lists = []
        for date in dates:
            url1 = url[sname] % (date.year, date.month, date.day)
            #print url1
            html = urllib2.urlopen(url1).read()
            #print html
            soup = BeautifulSoup(html, "lxml")
            trs = soup.find('table', {'class':'data2_s'})

            for tr in trs.findAll('tr')[2:]:
                dic = []
                tds = tr.findAll('td')
                if tds[1].string is None: 
                    break
                if re.search('s1',url1):
                    data_names = ['id','date','hour','air_pressure','precipitation','temperature','humidity','wind_velocity','wind_direction','sun_time','radiation','cloud']
                    #ota
                    if unicode(tds[0].string) ==unicode('24','shift_jis'):
                        tds[0] ='0'
                        datef = date+datetime.timedelta(days=1)
                        dic.append(datef.strftime("%Y/%m/%d") + ' ' + tds[0].zfill(2) + ":00")
                        dic.append(datef.strftime("%Y/%m/%d"))
                        dic.append(_str2float(tds[0]))
                    else:
                        dic.append(date.strftime("%Y/%m/%d") + ' ' + tds[0].string.zfill(2) + ":00")
                        dic.append(date.strftime("%Y/%m/%d"))
                        dic.append(_str2float(tds[0].string))
                    #print tds[0].string,type(tds[0].string)
                    dic.append(_str2float(tds[2].string))  # 気圧
                    dic.append(_str2float(tds[3].string))  # rain
                    dic.append(_str2float(tds[4].string))  # 気温
                    dic.append(_str2float(tds[7].string))  # 湿度
                    dic.append(_str2float(tds[8].string))  # wind
                    #dic.append(_str2string(tds[9].string))  # direction
                    dic.append(_mod_corruption(_str2string(tds[9].string)))  # direction
                    if tds[10].string == "" or tds[5].string == "--":
                        dic.append(0.0)
                    else:
                        dic.append(_str2float(tds[10].string))  # 日照時間
        #            dic.append(_str2float(tds[10].string))  # 日照時間
                    dic.append(_str2float(tds[11].string))  # swrad
                    cloud_ = re.match("\d*",_str2string(tds[15].string))
                    dic.append(cloud_.group())  # cloud

                else:
                    data_names = ['id','date','hour','precipitation','temperature','wind_velocity','wind_direction','sun_time']
                    if unicode(tds[0].string) ==unicode('24','shift_jis'):
                        tds[0] ='0'
                        datef = date+datetime.timedelta(days=1)
                        dic.append(datef.strftime("%Y/%m/%d") + ' ' + tds[0].zfill(2) + ":00")
                        dic.append(datef.strftime("%Y/%m/%d"))
                        dic.append(_str2float(tds[0]))
                    else:
                        dic.append(date.strftime("%Y/%m/%d") + ' ' + tds[0].string.zfill(2) + ":00")
                        dic.append(date.strftime("%Y/%m/%d"))
                        dic.append(_str2float(tds[0].string))
                    dic.append(_str2float(tds[1].string))  # rain
                    dic.append(_str2float(tds[2].string))  # temp
                    dic.append(_str2float(tds[3].string))  # wind 
                    #dic.append(_str2string(tds[4].string))  # direction
                    dic.append(_mod_corruption(_str2string(tds[4].string)))  # direction
                    if tds[5].string == "" or tds[5].string == "--":
                        dic.append(0.0) 
                    else:
                        dic.append(_str2float(tds[5].string))  # daytime
                lists.append(dic)

        import pandas as pd
        df = pd.DataFrame(data=lists, columns=data_names)
        df.index = df.id
        df.to_csv(outfile.format(sname, s_start, s_end), encoding='shift_jis', index=None)


def _str2float(str):
    if str:
        try:
            return float(str)
        except:
            return '--'
    else:
        return '--'


def _str2string(str):
    if str:
        try:
            return str.string
        except:
            return '--'
    else:
        return '--'


def _mod_corruption(str1):
    str1 = unicode(str1)
    delta = 22.5
    if str1 == u'北':
        str2 = delta * 0
    elif str1 == u'北北東':
        str2 = delta * 1
    elif str1 == u'北東':
        str2 = delta * 2
    elif str1 == u'東北東':
        str2 = delta * 3
    elif str1 == u'東':
        str2 = delta * 4
    elif str1 == u'東南東':
        str2 = delta * 5
    elif str1 == u'南東':
        str2 = delta * 6
    elif str1 == u'南南東':
        str2 = delta * 7
    elif str1 == u'南':
        str2 = delta * 8
    elif str1 == u'南南西':
        str2 = delta * 9
    elif str1 == u'南西':
        str2 = delta * 10
    elif str1 == u'西南西':
        str2 = delta * 11
    elif str1 == u'西':
        str2 = delta * 12
    elif str1 == u'西北西':
        str2 = delta * 13
    elif str1 == u'北西':
        str2 = delta * 14
    elif str1 == u'北北西':
        str2 = delta * 15
    elif str1 == u'静穏':
        str2 = delta * 16
    else:
        str2 = '--'
    return str2

if __name__ == '__main__':

    get_mp_wind('F:/okada/Data/mp/', year=2012, items=['C'])
    get_jma_wind('F:/okada/Data/jma/', year=2012)


# coding: utf-8

import pandas as pd
from datetime import datetime, timedelta

def prepare(station, csvfile):

    print station, csvfile

    parse = lambda d, h: datetime.strptime(d, '%Y-%m-%d') + timedelta(hours=int(h))
    df = pd.read_csv(csvfile, parse_dates={'datetime':['date','hour']}, na_values='*', date_parser=parse)
    df['station'] = station

    if station in [3, 4, 5, 6, 7, 12, 13]:
        vtypes = {'temperature':6, 'salilnity':7, 'DO':19, 'chlorophyll':10}
    elif station in [1, 2, 10, 11]:
        vtypes = {'temperature':6, 'salilnity':7}
    elif station in [8, 9]:
        vtypes = {'temperature':6}

    for k, v in vtypes.items():
        var = df[['datetime','station','depth',k]]
        var = var.dropna()
        var.columns = ['datetime','station', 'depth','value']
        var['type'] = v
        try:
            obs = obs.append(var)
        except:
            obs = var

    return obs

obs = prepare(1, '/Users/teruhisa/Dropbox/Data/obweb/db/akashi_q2.csv')
"""obs = obs.append(prepare(2, '/Users/teruhisa/Dropbox/Data/obweb/db/sumoto_q2.csv'))
obs = obs.append(prepare(3, '/Users/teruhisa/Dropbox/Data/obweb/db/kansaiAP_q1.csv'))
obs = obs.append(prepare(4, '/Users/teruhisa/Dropbox/Data/obweb/db/kobe_q1.csv'))
obs = obs.append(prepare(5, '/Users/teruhisa/Dropbox/Data/obweb/db/yodo_q1.csv'))
obs = obs.append(prepare(6, '/Users/teruhisa/Dropbox/Data/obweb/db/hannan_q1.csv'))
obs = obs.append(prepare(7, '/Users/teruhisa/Dropbox/Data/obweb/db/sakaihama_q1.csv'))
obs = obs.append(prepare(10, '/Users/teruhisa/Dropbox/Data/obweb/db/awaji_q2.csv'))
obs = obs.append(prepare(11, '/Users/teruhisa/Dropbox/Data/obweb/db/suma_q2.csv'))
obs = obs.append(prepare(12, '/Users/teruhisa/Dropbox/Data/obweb/db/osaka_q1.csv'))
obs = obs.append(prepare(13, '/Users/teruhisa/Dropbox/Data/obweb/db/kishiwada_q1.csv'))"""

obs.to_csv('/Users/teruhisa/Dropbox/Data/obweb/converted_obs_2012_small.csv', index=False)

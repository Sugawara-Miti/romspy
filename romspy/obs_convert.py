# coding: utf-8

# obs_convert (c) 2015 Teruhisa Okada

import pandas as pd
from datetime import datetime, timedelta
from romspy.O2_saturation import O2_saturation_mol


def convert(station, csvfile):

    print station, csvfile

    parse = lambda d, h: datetime.strptime(d, '%Y-%m-%d') + timedelta(hours=int(h))
    df = pd.read_csv(csvfile, parse_dates={'datetime':['date','hour']}, na_values='*', date_parser=parse)
    df['station'] = station

    if station in [3, 4, 5, 6, 7, 12, 13]:
        vtypes = {'temperature':6, 'salilnity':7, 'DO':15, 'chlorophyll':10}
        df.DO = df.DO / 100.0 * O2_saturation_mol(df.temperature, df.salilnity)
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

obs = convert(1, 'Z:/Data/obweb/db/akashi_q2.csv')
obs = obs.append(convert(2, 'Z:/Data/obweb/db/sumoto_q2.csv'))
obs = obs.append(convert(3, 'Z:/Data/obweb/db/kansaiAP_q1.csv'))
obs = obs.append(convert(4, 'Z:/Data/obweb/db/kobe_q1.csv'))
obs = obs.append(convert(5, 'Z:/Data/obweb/db/yodo_q1.csv'))
obs = obs.append(convert(6, 'Z:/Data/obweb/db/hannan_q1.csv'))
obs = obs.append(convert(7, 'Z:/Data/obweb/db/sakaihama_q1.csv'))
obs = obs.append(convert(10, 'Z:/Data/obweb/db/awaji_q2.csv'))
obs = obs.append(convert(11, 'Z:/Data/obweb/db/suma_q2.csv'))
obs = obs.append(convert(12, 'Z:/Data/obweb/db/osaka_q1.csv'))
obs = obs.append(convert(13, 'Z:/Data/obweb/db/kishiwada_q1.csv'))

obs.to_csv('Z:/Data/obweb/converted_db_oxygen3.csv', index=False)

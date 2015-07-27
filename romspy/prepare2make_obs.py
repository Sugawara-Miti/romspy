# coding: utf-8

import pandas as pd

def prepare2make_obs(csvfile, station, df=None):

    df2 = pd.read_csv(csvfile, parse_dates={'datetime':['date','hour']}, na_values='*')
    df2['station'] = station
    #df2['lon'] = 
    #df2['lat'] = 
    if df is not None:
        return df.append(df2)
    else:
        return df2

if __name__ == '__main__':
    datadir = "/Users/teruhisa/Dropbox/Data/obweb/db/"
    df = prepare2make_obs(datadir+'akashi_q2.csv', 1)
    df = prepare2make_obs(datadir+'awaji_q2.csv', 2, df)
    df = prepare2make_obs(datadir+'kansaiAP_q1.csv', 3, df)
    df = prepare2make_obs(datadir+'kobe_q1.csv', 4, df)
    df = prepare2make_obs(datadir+'yodo_q1.csv', 5, df)
    df = prepare2make_obs(datadir+'hannan_q1.csv', 6, df)
    df = prepare2make_obs(datadir+'sakaihama_q1.csv', 7, df)
    df = prepare2make_obs(datadir+'awaji_q2.csv', 10, df)
    df = prepare2make_obs(datadir+'suma_q2.csv', 11, df)
    df = prepare2make_obs(datadir+'osaka_q1.csv', 12, df)
    df = prepare2make_obs(datadir+'kishiwada_q1.csv', 13, df)

    #prepare2make_obs('/Users/teruhisa/Dropbox/Data/obweb/download/', station=8)
    #prepare2make_obs('/Users/teruhisa/Dropbox/Data/obweb/download/', station=9)

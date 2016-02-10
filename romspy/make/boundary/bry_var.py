# coding: utf-8
# bry_var (c) 2015-10-14 Teruhisa Okada

import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np

__version__ = 1.0


def bry_var(dims, varfiles, dates, rule=None):
    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    s_rho   = dims['s']

    df = {}
    for vname in varfiles.keys():
        print vname
        parse = lambda date: datetime.datetime.strptime(date, '%Y/%m/%d %H:%M')
        df[vname] = pd.read_csv(varfiles[vname], index_col=0, date_parser=parse, header=[0,1])
        print df[vname].columns
    var = pd.concat([df[vname] for vname in varfiles.keys()], axis=1)
    if rule == 'M':
        var.plot(ax=plt.gca(), title='before')
        var = var.resample('M', how='mean', loffset=-datetime.timedelta(days=15))
    elif rule == 'D':
        var.plot(ax=plt.gca(), title='before')
        var = var.resample('D', how='mean')
    var = var.interpolate()
    var = var[var.index >= dates[0]]
    var = var[var.index <= dates[-1]]
    var.plot(title='after')

    time = var.index
    out = {}
    for vname in var.columns.levels[0]:
        v = var[vname]
        print vname, '\n', v
        var_south = np.zeros([len(time), s_rho, xi_rho])
        var_west = np.zeros([len(time), s_rho, eta_rho])

        for t, i in enumerate(v.index):
            for x in range(xi_rho):
                var_south[t, :, x] = np.linspace(v.south_bot[i], v.south_sur[i], s_rho)
            for y in range(eta_rho):
                var_west[t, :, y] = np.linspace(v.west_bot[i], v.west_sur[i], s_rho)

        out[vname] = {'s':var_south, 'w':var_west}

    if len(out) == 1:
        return out[vname], time.to_pydatetime()
    else:
        return out, time.to_pydatetime()


if __name__ == '__main__':
    dims = {'xi':5, 'eta':5, 's':20}
    dates = [datetime.datetime(2012, 1, 1, 0), datetime.datetime(2013, 1, 1, 0)]

    temp = {}
    temp['south_bot'] = 'V:/ROMS/boundary/temp_south_bot_A11_2012.csv'
    temp['south_sur'] = 'V:/ROMS/boundary/temp_south_sur_A11_2012.csv'
    temp['west_bot'] = 'V:/ROMS/boundary/temp_west_bot_akashi_2012.csv'
    temp['west_sur'] = 'V:/ROMS/boundary/temp_west_sur_akashi_2012.csv'
    temp = bry_var(dims, temp, dates, 'D')

    bio = {}
    bio['west'] = 'V:/ROMS/boundary/bio_west_seto_2001-2013_15D.csv'
    bio['south'] = 'V:/ROMS/boundary/bio_south_seto_2001-2013_15D.csv'
    bio['others'] = 'V:/ROMS/boundary/bio_others.csv'
    bio = bry_var(dims, bio, dates)

    plt.show()

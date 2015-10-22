# -*- coding: utf-8 -*-

"""
Program to make bry nc file
okada on 2014/10/21
"""

import numpy as np
import pandas as pd


def bry_wq_csv(dims, vname, wqfiles, dates=['2012-01-01','2013-01-01']):
    xi_rho  = dims['xi']
    eta_rho = dims['eta']
    s_rho   = dims['s']
    var_out = {}
    for d in wqfiles.keys():
        print 'bry_wq_csv:', vname, d, wqfiles[d]
        sta = pd.read_csv(wqfiles[d], parse_dates='time', index_col='time')
        sta = sta.resample('D')
        # sta = sta.interpolate('polynomial', axis=1) # , order=3)
        sta[vname][dates[1]] = sta[vname][dates[0]]
        sta = sta.interpolate()
        td = len(sta)    
        if d == 'w':
            length = eta_rho
        elif d == 's':
            length = xi_rho
        var_out[d] = np.ndarray(shape=[td, s_rho, length])
        for l in xrange(length):
            for s in xrange(s_rho):
                var_out[d][:, s, l] = sta[vname]
    return var_out


if __name__ == '__main__':    
    dims = {'xi':2, 'eta':2, 's':2}
    wqfiles = {'w':'../wq/akashi/wq_2012.csv',
               's':'../wq/sumoto/wq_2012.csv'}
    temp_out = bry_wq_csv(dims, 'temp', wqfiles, dates=['2012-01-01','2013-01-01'])

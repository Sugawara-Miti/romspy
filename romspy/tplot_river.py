# -*- coding: utf-8 -*-

"""
Title: plot river variables
Author: okada
Created on Tue Dec 17 18:05:24 2013
"""

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.dates import DateFormatter

def tplot_river(ncfile, figdir, vname, rivername):

    print ncfile, figdir, vname, rivername

    nc = netCDF4.Dataset(ncfile, 'r')
    
    start = 0 #7*30*24
    end   = -1 #11*30*24

    if rivername == 'Yodo': iriver = 0
    
    var   = abs(nc.variables[vname][start:end,iriver])
    vunit = nc.variables[vname].units
    tname = nc.variables[vname].time
    time  = nc.variables[tname][start:end]
    tunit = nc.variables[tname].units
    nc.close()

    dtime = netCDF4.num2date(time, tunit)
    year  = str(dtime[0].year)

    fig, ax = plt.subplots()

    ax.plot(dtime, var)

    ax.xaxis.set_major_formatter( DateFormatter('%m-%d') )
    ax.set_xlabel(year)
    ax.set_ylabel(vunit)

    ax.legend(loc='best')
    ax.set_title('Time series of {}, {} River, {}'.format(vname, rivername, year))    
    fig.savefig(figdir + 'tplot_{}.png'.format(vname), bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':

    tplot_river('test/nc/ob500_river_fennel_2012_2.nc',
                './',
                'river_transport',
                'Yodo')

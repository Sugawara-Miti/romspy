# -*- coding: utf-8 -*-

"""
2013/12/17 okada created this file.
2015/05/01 okada remake it.
"""

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.dates import DateFormatter

def tplot_frc(frcfile, figdir, vname):

    print frcfile, figdir, vname

    nc = netCDF4.Dataset(frcfile, 'r')
    timename = nc.variables.keys()[0]
    
    print len(nc.dimensions[timename])
    start = 6*30*24
    end   = 11*30*24
    
    time  = nc.variables[timename][start:end]
    tunit = nc.variables[timename].units
    var   = nc.variables[vname][start:end,100,100]
    vunit = nc.variables[vname].units
    nc.close()

    dtime = netCDF4.num2date(time, tunit)

    fig, ax = plt.subplots()

    ax.plot(dtime, var)

    ax.xaxis.set_major_formatter( DateFormatter('%m-%d') )
    ax.set_xlabel('2012')
    ax.set_ylabel(vunit)

    ax.legend(loc='best')
    ax.set_title('Time series of {}'.format(vname))
    
    plt.show()
    #fig.savefig(figdir + 'tplot_frc_{}.png'.format(vname), bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':

    tplot_frc('test/nc/ob500_frc_rain_2012.nc', './', 'rain')

# coding: utf-8
# (c) 2016-02-10 Teruhisa Okada

import netCDF4
import numpy as np


if __name__ == '__main__':

    grdfile = '/home/okada/Data/ob500_grd-11_3.nc'
    
    grd = Grid(grdfile)
    
    print grd

# -*- coding: utf-8 -*-

"""
Tests of romspy.hview (c) 2015-08-14 Teruhisa Okada
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import hview
import romspy


def _grd():
    ncfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-9.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    romspy.hview(ncfile, 'h', interval=np.arange(-10,0.1,5), mapfile=mapfile, cff=-1)
    plt.savefig("test_hview_grd.png")


def _test2():
    time = datetime(2012, 8, 5, 0)
    ncfile = '/Users/teruhisa/mnt/apps/OB500_fennelP/I4DVAR/ob500_ini.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview(ncfile, 'temp', time, 20, mapfile=mapfile, figfile="hview_test2.png")


def _ini_diff3():
    ncfile = '/Users/teruhisa/mnt/data/is4dvar_out/03/ob500_ini_0.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview.ini_diff(ncfile, 'oxygen', 20, mapfile=mapfile, figfile="test_hview_ini_diff3.png")#, interval=np.arange(-1.0,1.1,1)


def _ini_diff4():
    ncfile = '/Users/teruhisa/mnt/apps/OB500_fennelP/IS4DVAR03/ob500_ini_0.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview.ini_diff(ncfile, 'oxygen', 20, mapfile=mapfile, figfile="test_hview_ini_diff3.png")#, interval=np.arange(-1.0,1.1,1)


def _test4():
    ncfile = '/home/okada/roms/Apps/OB500A/I4DVAR01/ob500a_ini.nc'
    mapfile = '/home/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview.ini_diff(ncfile, 'temp', 20, mapfile=mapfile, figfile="hview_test4.png", interval=np.arange(-1.0,1.1,2))


def _test5():
    time = datetime(2012, 1, 1, 0)
    ncfile = '/home/okada/Dropbox/Data/ob500a_std_i_fennelP-3.nc'
    mapfile = '/home/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    print romspy.get_time(ncfile)
    romspy.hview(ncfile, 'temp', time, 20, mapfile=mapfile, figfile="hview_test5.png")


def _test6():
    time = datetime(2012, 8, 5, 0)
    ncfile = '/home/okada/roms/Apps/OB500A/Normalization/ob500a_nrm_i.nc'
    mapfile = '/home/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    print romspy.get_time(ncfile)
    romspy.hview(ncfile, 'chlorophyll', time, 20, mapfile=mapfile, figfile="hview_test6.png")


if __name__ == '__main__':
    _ini_diff4()

# -*- coding: utf-8 -*-

"""
Tests of romspy.hview (c) 2015-08-14 Teruhisa Okada
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import hview
import romspy


def _test1():
    time = datetime(2012, 3, 5, 12)
    ncfile = '/Users/teruhisa/Dropbox/Data/OB500_fennelP/NL02/ob500_dia_0003.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview(ncfile, 'SOD', time, interval=np.arange(-30,1,5), mapfile=mapfile)
    plt.savefig("hview_test.png")


def _test2():
    time = datetime(2012, 8, 5, 0)
    ncfile = '/Users/teruhisa/mnt/apps/OB500_fennelP/I4DVAR/ob500_ini.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview(ncfile, 'temp', time, 20, mapfile=mapfile, figfile="hview_test2.png")


def _test3():
    ncfile = '/Users/teruhisa/mnt/apps/OB500_fennelP/I4DVAR01/ob500_ini.nc'
    mapfile = '/Users/teruhisa/Dropbox/Data/deg_OsakaBayMap_okada.bln'
    hview.ini_diff(ncfile, 'temp', 20, interval=np.arange(-1.0,1.1,1), mapfile=mapfile, figfile="hview_test3.png")


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
    _test6()

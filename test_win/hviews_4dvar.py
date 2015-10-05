# coding: utf-8

"""
hviews for 4dvar (c) 2015-09-26 Teruhisa Okada
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import romspy

#ncfile = 'F:/okada/Dropbox/Data/ob500_grd-9.nc'
ncfile = 'Z:/roms/Apps/OB500_fennelP/4DVAR04/output/ob500_ini_0.nc'
mapfile = 'F:/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'

t = datetime(2012, 8, 5)

#romspy.hview(ncfile, 'h', mapfile=mapfile, cff=-1)  #, interval=np.arange(-10,0.1,5)
romspy.hview(ncfile, 'oxygen', t, 1, mapfile=mapfile, cff=-1, interval=np.arange(0.0,300.1,50))
plt.savefig("hviews_4dvar.png", bbox_inches='tight')

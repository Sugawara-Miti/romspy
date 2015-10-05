# -*- coding: utf-8 -*-

"""
Tests of romspy.hview (c) 2015-08-14 Teruhisa Okada
"""

import numpy as np
import romspy

ncfile = 'Z:/roms/Apps/OB500_fennelP/NL07/ob500_dia_0004.nc'
mapfile = 'F:/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'

dia = romspy.hview.Dataset(ncfile, mapfile=mapfile)
dia.print_time('all')
print dia.get_varname(ndim=3)

for vname in dia.get_varname(ndim=3):
    dia.hview(vname, time=3, interval=np.arange(-100.0,0.1,50))
    dia.hview(vname, time=3, interval=np.arange(-100.0,0.1,50))
    dia.hview(vname, time=3, interval=np.arange(-100.0,0.1,50))
    dia.savefig('hview_{}.png'.format(vname))

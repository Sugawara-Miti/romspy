# -*- coding: utf-8 -*-

"""
Tests of romspy.hview (c) 2015-08-14 Teruhisa Okada
"""

import numpy as np
import romspy

ncfile = 'Z:/roms/Apps/OB500_fennelP/NL07/ob500_avg.nc'
mapfile = 'F:/okada/Dropbox/Data/deg_OsakaBayMap_okada.bln'

dia = romspy.hview.Dataset(ncfile, mapfile=mapfile)
dia.print_time('all')
print dia.get_varname(ndim=4)

for vname in dia.get_varname(ndim=4):
    if vname not in ['u', 'v']:
        dia.hview(vname, time=7, k=1)#, interval=np.arange(-100.0,0.1,50))
        dia.savefig('{}_{}_{}.png'.format(ncfile[:-3], vname, 1))

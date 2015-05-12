# -*- coding: utf-8 -*-

import romspy

romspy.hview('nc/ob500_grd-v5.nc',
             'ob500_grd-v5.png',
             vname='h',
             cblabel='Depth[m]',
             vmax=0, vmin=-120, interval=20, cff=-1,
             obsfile='nc/ob500_obs_tsdc.nc')

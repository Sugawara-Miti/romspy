# -*- coding: utf-8 -*-

"""
2015/05/01 okada make this file.
"""

from hview import hview

ncfile = 'test/nc/ob500_rst.nc'
pngfile = 'ob500_rst_temp.png'

hview(ncfile, pngfile, 'temp', k=1, cblabel='Temperature[C]')

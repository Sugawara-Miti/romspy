# coding: utf-8
# (c) 2015-11-06 Teruhisa Okada

import datetime
import romspy

infile = 'ob500_his_0004.nc'
outfile = 'ob500_ini_his_0804.nc'

print romspy.get_time(infile, 'all')

date = datetime.datetime(2012, 8, 4, 0, 0, 0)
#redate = datetime.datetime(2012, 4, 1, 0, 0, 0)

romspy.his2ini(infile, outfile, date)

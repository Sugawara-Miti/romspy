# coding: utf-8
# (c) 2015-08-01 Teruhisa Okada

import netCDF4
import romspy


def get_time(ncfile, which='ends', t=None, name='ocean_time'):
    """
    2015-11-09　ncfile が nc でも可能に
    """
    print "\nromspy.get_time()"
    if type(ncfile) == netCDF4.Dataset:
        nc = ncfile
    else:
        nc = netCDF4.Dataset(ncfile, 'r')
    if t is not None:
        print netCDF4.num2date(nc.variables[name][t], romspy.JST), t
    elif which == 'ends':
        t = len(nc.dimensions[name])
        start = nc.variables[name][0]
        end = nc.variables[name][t-1]
        print netCDF4.num2date(start, romspy.JST), 0
        print netCDF4.num2date(end, romspy.JST), t-1
    elif which == 'all':
        time = nc.variables[name][:]
        for t in range(len(time)):
            print netCDF4.num2date(time[t], romspy.JST), t
    else:
        print 'ERROR: You should select "ends" or "all"'

if __name__ == '__main__':
    import netCDF4
    ncfile = 'F:/okada/Dropbox/Data/ob500_ini_test.nc'
    nc = netCDF4.Dataset(ncfile)
    get_time(nc)

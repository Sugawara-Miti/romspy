# coding: utf-8
# (c) 2015-08-04 Teruhisa Okada  

import netCDF4

__version__ = 0.1  # 2015-10-27


def get_vnames(ncfile, ndim=None):
    if type(ncfile) == str:
        nc = netCDF4.Dataset(ncfile, 'r')
        print ncfile
    else:
        nc = ncfile
    if ndim is not None:
        varnames = []
        for vname in nc.variables.keys():
            if nc.variables[vname].ndim == ndim:
                varnames.append(vname)
        print varnames
    else:
        print nc.variables.keys()

if __name__ == '__main__':
    get_vnames('Z:/apps/OB500P/case15/NL/ob500_dia_0004.nc', 4)


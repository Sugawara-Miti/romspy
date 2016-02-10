# coding: utf-8
# (c) 2015-11-23 Teruhisa Okada

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import shutil
import os.path
import romspy
romspy.cmap('jet')


def get_vstd(ncfile_ens, ncfile_tru, N, vnames, plot=False):
    ini = netCDF4.Dataset(ncfile_tru, 'r')
    var = {}
    for i in range(N):
        ncfile = ncfile_ens.format(i)
        print ncfile, vnames
        nc = netCDF4.Dataset(ncfile, 'r')
        for vname in vnames:
            v = nc.variables[vname]
            vini = ini.variables[vname]
            if v.ndim == 4:
                if i == 0:
                    tend, kend, jend, iend = v.shape
                    var[vname] = np.zeros([N, kend, jend, iend])
                var[vname][i,:,:,:] = v[-1,:,:,:] - vini[-1,:,:,:]

    vstd = {}
    for vname in var.keys():
        vstd[vname] = np.std(var[vname], axis=0)

        if plot is True:
            plt.figure(figsize=[12,5])
            plt.subplot(121)
            vmax = np.max(vstd[vname])
            vmin = np.min(vstd[vname])
            plt.pcolor(vstd[vname][19,:,:], vmax=vmax, vmin=vmin)
            plt.colorbar()
            plt.title('surface '+vname)
            plt.subplot(122)
            plt.pcolor(vstd[vname][0,:,:], vmax=vmax, vmin=vmin)
            plt.colorbar()
            plt.title('bottom '+vname)
            plt.show()

    return vstd


def make_std_file(stdfile, vstd, base=None):
    if base is not None:
        print base, '=>', stdfile
        shutil.copyfile(base, stdfile)
    for vname in vstd.keys():
        romspy.edit_nc_var(stdfile, vname, vstd[vname], t=-1)


if __name__ == '__main__':

    case = '21_NLS3'
    
    if case == '1_NLS2':
        ncfile_ens = '/home/okada/ism-i/apps/OB500P/case21/NLS2/runs/run{}/ob500_rst.nc'
        ncfile_tru = '/home/okada/ism-i/apps/OB500P/case21/NLS2/ob500_rst.nc'
        ncfile_std = '/home/okada/ism-i/data/ob500_std_i_case21_NLS2_100.nc'
        N = 100
    elif case == '21_NLS3':
        ncfile_ens = '/home/okada/ism-i/apps/OB500P/case21/NLS3/runs/run{}/ob500_rst.nc'
        ncfile_tru= '/home/okada/ism-i/apps/OB500P/case21/NLS3/ob500_rst.nc'
        ncfile_std = '/home/okada/ism-i/data/ob500_std_i_case21_NLS3_100.nc'
        N = 100
    vnames = ['temp', 'salt', 'chlorophyll', 'oxygen', 'NH4', 'NO3', 'PO4', 'LdetritusN', 'SdetritusN', 'LdetritusP', 'SdetritusP', 'phytoplankton', 'zooplankton']
    #vnames = ['salt']
    vstd = get_vstd(ncfile_ens, ncfile_tru, N, vnames)  # , plot=True)

    basefile = '/home/okada/ism-i/data/ob500_ini_zero_0101_grd-11_3.nc'
    make_std_file(ncfile_std, vstd, base=basefile)

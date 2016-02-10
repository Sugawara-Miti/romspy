# coding: utf-8
# (c) 2015-11-25 Teruhisa Okada

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.colors import LogNorm
import romspy


def tplot_rmse(obsfile, modfiles, varid):
    obs = netCDF4.Dataset(obsfile, 'r')
    obs_type = obs['obs_type'][:]

    fig, ax = plt.subplots(1,2,figsize=(9,4))
    cff = 1.0
    if varid == 6:
        lim = [20,30]
        title = 'Temperature[degC]'
    elif varid == 7:
        lim = [23,33]
        title = 'Salinity'
    elif varid == 10:
        #cff = 1.92
        lim = [0,30]
        title = 'Chlorophyll[micro mol/l]'
    elif varid == 15:
        cff = romspy.mol2g_O2
        lim = [0,12]
        title = 'DO[mg/l]'

    ax = plt.gca()

    for modfile in modfiles:
        print obsfile, modfile, varid
        mod = netCDF4.Dataset(modfile, 'r')
        mod_value = mod['NLmodel_value'][:]
        index = np.where((mod_value<999) & (mod_value>0) & (obs_type==varid))
        obs_value = obs['obs_value'][index]
        mod_value = mod_value[index]
        mod_initial = mod['NLmodel_initial'][index]

        df

        ax.plot(mod_initial, obs_value)
        ax[1].scatter(mod_value, obs_value)

    for i in range(2):
        ax[i].plot([0,100], [0,100], 'k-', alpha=0.5)
        ax[i].set_xlabel('Model')
        ax[i].set_xlim(lim)
        ax[i].set_ylim(lim)
    ax[0].set_ylabel('Observation')
    ax[0].set_title('Background')
    ax[1].set_title('Assimilation')
    plt.suptitle(title)

if __name__ == '__main__':
    #import seaborn as sns
    romspy.cmap('jet')

    case = 'case28/DA0-3.1'

    varids = [6,7,10,15]
    #varids = [6,7]
    #varids = [6]
    obsfile = '/home/okada/Data/ob500_obs_2012_mp-2.nc'
    #obsfile = '/home/okada/Data/ob500_obs_2012_mp-1_ts.nc'
    #modfile = '/home/okada/ism-i/apps/OB500P/{}/output/ob500_mod_0.nc'.format(case)
    modfiles = ['/home/okada/ism-i/apps/OB500P/{}/output/ob500_mod_{}.nc'.format(case, i*24) for i in range(0,7)]

    for varid in varids:
        tplot_rmse(obsfile, modfiles, varid)
        #plt.show()
        romspy.savefig('/home/okada/Dropbox/Figures/OB500P/{}/tplot_rmse_{}.png'.format(case, varid))

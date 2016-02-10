# coding: utf-8
# (c) 2015-11-25 Teruhisa Okada

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.colors import LogNorm
import romspy


def plot_hist2d(obsfile, modfiles, varid, how):
    print obsfile, modfiles[0], varid
    obs = netCDF4.Dataset(obsfile, 'r')
    obs_type = obs['obs_type'][:]

    mod = netCDF4.Dataset(modfiles[0], 'r')
    mod_value = mod['NLmodel_value'][:]
    index = np.where((mod_value<999) & (mod_value>0) & (obs_type==varid))
    obs_value = obs['obs_value'][index]
    mod_value = mod_value[index]
    mod_initial = mod['NLmodel_initial'][index]

    for modfile in modfiles[1:]:
        print obsfile, modfile, varid
        mod = netCDF4.Dataset(modfile, 'r')
        mod_value_1 = mod['NLmodel_value'][:]
        index = np.where((mod_value_1<999) & (mod_value_1>0) & (obs_type==varid))
        obs_value = np.append(obs_value, obs['obs_value'][index])
        mod_value = np.append(mod_value, mod_value_1[index])
        mod_initial = np.append(mod_initial, mod['NLmodel_initial'][index])

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

    obs_value = np.append(cff*obs_value, [-1,50])
    mod_value = np.append(cff*mod_value, [-1,50])
    mod_initial = np.append(cff*mod_initial, [-1,50])

    if how == 'scatter2d':
        ax[0].scatter(mod_initial, obs_value)
        ax[1].scatter(mod_value, obs_value)

    elif how == 'scatter2d_gaussian':
        h2 = {}
        for i, mod in enumerate([mod_initial, mod_value]):
            xy = np.vstack([mod, obs_value])
            z = gaussian_kde(xy)(xy)
            if i == 0:
                vmax = z.max()
            h2[i] = ax[i].scatter(mod, obs_value, c=z, s=10, edgecolor='', vmin=0, vmax=vmax)
            #plt.colorbar(h2[i])

    elif how == 'hist2d':
        for i, mod in enumerate([mod_initial, mod_value]):
            h2 = ax[i].hist2d(mod, obs_value, bins=500, norm=LogNorm(), vmin=1, vmax=1e2)
            #plt.colorbar(h2)

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

    #how = 'scatter2d'
    how = 'scatter2d_gaussian'
    #how = 'hist2d'
    varids = [6,7,10,15]
    #varids = [6,7]
    #varids = [6]
    obsfile = '/home/okada/Data/ob500_obs_2012_mp-2.nc'
    #obsfile = '/home/okada/Data/ob500_obs_2012_mp-1_ts.nc'
    #modfile = '/home/okada/ism-i/apps/OB500P/{}/output/ob500_mod_0.nc'.format(case)
    modfiles = ['/home/okada/ism-i/apps/OB500P/{}/output/ob500_mod_{}.nc'.format(case, i*24) for i in range(0,7)]

    for varid in varids:
        plot_hist2d(obsfile, modfiles, varid, how)
        #plt.show()
        romspy.savefig('/home/okada/Dropbox/Figures/OB500P/{}/{}_{}.png'.format(case, how, varid))

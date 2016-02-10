# coding: utf-8
# (c) 2016-01-27 Teruhisa Okada

import netCDF4
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pandas as pd
import romspy


def plot_pdf_param(inifiles, vname, ax=plt.gca()):
    for inifile in inifiles:
        print inifile,
        nc = netCDF4.Dataset(inifile, 'r')
        param = nc[vname][:]
        print param
        if 'params' not in locals():
            params = param[0]
        else:
            params = np.append(params, param[0])
    #ax.hist(params)
    sns.distplot(params, rug=True, kde=False)
    ax.set_xlabel(vname)
    plt.grid(None)

    pmean = np.mean(params)
    pmedian = np.median(params)
    #ax.text(0.1,0.1,'mean={}'.format(pmean), transform=ax.transAxes)
    text = AnchoredText('mean={:.2e}'.format(pmean), loc=1)
    ax.add_artist(text)


def main(test):
    if test == 'param2':
        inifiles = ['/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_ini_{}.nc'.format(test, i) for i in range(0,8712,24)]
        title = '4dvar(ini+param), window=1day, pfactor=0.1'
        for vid in [1,4]:
            vname = 'P{:02d}'.format(vid)
            figfile = '/home/okada/Dropbox/Figures/2016_param/plot_pdf_param_{test}_{vname}.png'.format(**locals())
            plt.cla()
            plot_pdf_param(inifiles, vname)
            plt.title(title)
            romspy.savefig(figfile)


if __name__ == '__main__':
    import seaborn as sns
    main('param2')
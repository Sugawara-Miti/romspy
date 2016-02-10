# coding: utf-8
# (c) 2015-11-24 Teruhisa Okada

import netCDF4
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np


def plot_cost(modfiles, Ninner=10, plot='J', legend=False):
    fig, ax = plt.subplots(1,1,figsize=[6,5])
    for modfile in modfiles:
        print modfile.decode('utf-8')
        nc = netCDF4.Dataset(modfile.decode('utf-8'))
        jb = nc.variables['back_function'][:]
        jo = nc.variables['TLcost_function'][:]
        j = jb + jo
        if 'J' in plot:
            ax.semilogy(j, '.-', label='J')
        if 'b' in plot:
            ax.semilogy(jb, '.-', label='Jb')
        if 'o' in plot:
            ax.semilogy(jo, '.-', label='Jo')

    #ax.set_ylim(jo.min(), j.max())
    ax.set_xlim(0, Ninner)
    ax.set_ylabel('Cost function')
    ax.set_xlabel('iteration')
    #ax.set_title('n = 50')
    if legend:
        ax.legend()


def _test(test=1, hmax=None, hours=24):
    if test == 1:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/param1_2/output/ob500_mod_{}.nc'.format(i) for i in range(0,2208,24)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_param1_{}.png'.format(test+1)
        #modfiles = modfiles[-5:-4]
        plot_cost(modfiles,  Ninner=10, plot='bo')
        #plot_cost(modfiles,  Ninner=10, plot='Jbo', legend=True)
    elif test == 2:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/param1_3/output/ob500_mod_{}.nc'.format(i) for i in range(0,8784,24)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_param1_{}.png'.format(test+1)
        plot_cost(modfiles,  Ninner=20, plot='bo')
    elif test == 3:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/param1_4/output/ob500_mod_{}.nc'.format(i) for i in range(0,5448,24)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_param1_{}.png'.format(test+1)
        plot_cost(modfiles,  Ninner=15, plot='bo')
    elif test == 4:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/param1_4/output/ob500_mod_{}.nc'.format(i) for i in range(0,3120,24)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_param1_{}_3120.png'.format(test+1)
        plot_cost(modfiles,  Ninner=15, plot='bo')
    elif test == 'param2':
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_mod_{}.nc'.format(test, i) for i in range(0,8712,24)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_{}.png'.format(test)
        plot_cost(modfiles,  Ninner=15, plot='bo')
    elif 'param3' in test:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_mod_{}.nc'.format(test, i) for i in range(0,1104,24)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_{}.png'.format(test)
        plot_cost(modfiles,  Ninner=15, plot='bo')
    elif 'param4' in test:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_mod_{}.nc'.format(test, i) for i in range(0,48,24)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_{}.png'.format(test)
        plot_cost(modfiles,  Ninner=3, plot='bo')
    elif 'param5' in test:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_mod_{}.nc'.format(test, i) for i in range(0,hmax,hours)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_{}.png'.format(test)
        plot_cost(modfiles,  Ninner=15, plot='bo')
    elif 'param' in test:
        modfiles = ['/home/okada/ism-i/apps/OB500P/testDA/{}/output/ob500_mod_{}.nc'.format(test, i) for i in range(0,hmax,hours)]
        figfile = '/home/okada/Dropbox/Figures/2016_param/plot_cost_{}.png'.format(test)
        plot_cost(modfiles,  Ninner=15, plot='bo')

    romspy.savefig(figfile)
    plt.show()

if __name__ == '__main__':
    import seaborn as sns
    import romspy

    #_test(2)
    #_test('param5-05', hmax=384)
    #_test('param5-01', hmax=672)
    #_test('param5-005', hmax=672)
    #_test('param5-001', hmax=456)
    #_test('param5-001-hev', hmax=456)
    #_test('param5-001-7days', hmax=672, hours=24*7)
    _test('param6-ini', hmax=24, hours=24)

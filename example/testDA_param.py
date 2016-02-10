# coding: utf-8
# (c) 2015-11-24 Teruhisa Okada

import matplotlib.pyplot as plt
#import seaborn as sns
import os
import datetime
import romspy

# swithes

plot_cost = False

tplot_valification = False

hview_diff = True

tplot_rmse = False

# case name

case = 'testDA/param6-ini'

# date
period = 'day'
dates = [datetime.datetime(2012,1,1,0), datetime.datetime(2012,1,2,0)]

# input files
modfiles = ['/home/okada/ism-i/apps/OB500P/{}/output/ob500_mod_{}.nc'.format(case, i*24) for i in range(1)]
modfile = modfiles[0]
inifile = '/home/okada/ism-i/apps/OB500P/{}/output/ob500_ini_0.nc'.format(case)
obsfile = '/home/okada/Data/ob500_obs_2012_mp-3_clean.nc'
mapfile = '/home/okada/Dropbox/Maps/deg_OsakaBayMap_okada.bln'

# output files
plot_costfile = 'plot_costs.png'
tplot_va_tmpfile = 'tplot_va_{}.png'  # 'tplot_va_{}_week3.png'
hview_difffile = 'hview_diff_{}_{}.png'

# parameters
varids = [6,7,10,15]  # [6,7]
vnames = ['temp','salt','chlorophyll','oxygen']  # ['temp','salt']
stations = [3,4,5,6,12,13]
Ninner = 30

#===================================================================================
# resample parameters
if period == 'day':
    date_format = '%H:%M'
    resample = 'H'
elif period == 'week':
    date_format = '%m/%d'
    resample = 'H'

# outpt directories
outdir = os.path.dirname(modfiles[0]).replace('ism-i/apps', 'Dropbox/Figures')
outdir = outdir.replace('/output', '')
if not os.path.exists(outdir):
    print 'mkdir', outdir
    os.makedirs(outdir)

# plot cost functions
if plot_cost:
    romspy.plot_cost(modfiles, Ninner)
    outfile = os.path.join(outdir, plot_costfile)
    print outfile
    plt.suptitle(case)
    romspy.savefig(outfile)

# plot time series of mod files
assimilation = True
if tplot_valification:
    for varid in varids:
        fig, axes = plt.subplots(3,2, figsize=[12,12])
        axlist = [axes[y][x] for x in range(2) for y in range(3)]
        for station, ax in zip(stations, axlist):
            romspy.tplot_valification(obsfile, modfile, varid, station, dates, assimilation=assimilation, ax=ax, date_format=date_format, resample=resample)
            if varid == 6:
                ax.set_ylim(5, 30)
            elif varid == 7:
                ax.set_ylim(23, 33)
            elif varid == 10:
                ax.set_ylim(0, 30)
            elif varid == 15:
                ax.set_ylim(0, 12)
        outfile = os.path.join(outdir, tplot_va_tmpfile.format(varid))
        print outfile
        plt.suptitle(case)
        romspy.savefig(outfile)

# plot horizontal view of initial files
if hview_diff:
    romspy.cmap('jet')
    ini = romspy.Hview(inifile, mapfile=mapfile)
    for vname in vnames:
        for k in [1,20]:
            fig, axes = plt.subplots(1,2, figsize=[13,5])
            plt.subplot(121)
            ini.hview(vname, time=-1, k=k)
            plt.subplot(122)
            ini.hview(vname, time=0, k=k)
            plt.suptitle(case)
            outfile = os.path.join(outdir, hview_difffile.format(vname, k))
            print outfile
            romspy.savefig(outfile)

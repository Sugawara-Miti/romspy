# coding: utf-8
# (c) 2015-09-26 Teruhisa Okada

import matplotlib.pyplot as plt
import numpy as np
import romspy

import his


def _convert_address(filename):
    return filename.replace('/home/okada', 'Z:')


if __name__ == '__main__':
    import os
    romspy.cmap('jet')
    mapfile = '/home/okada/Dropbox/Maps/deg_OsakaBayMap_okada.bln'
    case = 'case24/NL5'
    avgfile = '/home/okada/Data/ob500_std_i_case21_NLS3_100.nc'

    if os.name == 'nt':
        mapfile = _convert_address(mapfile)
        avgfile = _convert_address(avgfile)

    time = 0
    k = 20
    vname = 'salt'

    outdir = os.path.dirname(avgfile).replace('ism-i/apps', 'Dropbox/Figures')
    outdir = outdir.replace('/output', '')
    if not os.path.exists(outdir):
        print 'mkdir', outdir
        os.makedirs(outdir)

    his = his.Dataset(avgfile, mapfile=mapfile)
    his.print_time('all')
    his.print_varname(4)

    levels = np.linspace(0, 1, 11)
    romspy.cmap('Blues')
    #his.hview(vname, time=time, k=k, levels=levels, method='contour_pcolor', fmt='%.1f')
    #his.hview(vname, time=time, k=k, levels=levels, method='contour_fill', fmt='%.1f')
    his.hview(vname, time=time, k=k, levels=levels, method='rbf', fmt='%.1f')
    plt.show()
    t = time+1
    fname = '{vname}_{t}_{k}.png'.format(**locals())
    #romspy.savefig(os.path.join(outdir, fname))
    plt.clf()

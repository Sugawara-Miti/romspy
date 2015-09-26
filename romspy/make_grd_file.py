# coding: utf-8

import matplotlib.pyplot as plt
import csv
import numpy as np


def _get_h(csvfile, x_rho, y_rho, check=None):

    h = np.zeros([y_rho, x_rho])
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for y, row in enumerate(reader):
            h[y_rho-y-1, :] = row[1:]
    if check is not None:
        plt.pcolor(h)
        plt.colorbar()
    return h


def make_grd_file(grdfile, meshfile, masklinesfile, geo=True, smoother='Laplacian'):

    print 'inporting pyroms ..'
    import pyroms

    name = 'ob500_grd'
    x_rho = 117
    y_rho = 124
    lon = [134.81541, 135.45423]
    lat = [34.16308, 34.717595]
    N = 20
    theta_b = 0
    theta_s = 3
    Tcline = 0.5
    f = 8.2606e-05
    rx0max = 0.15

    # hgrid

    hraw = _get_h(meshfile, x_rho, y_rho)
    h = hraw[:,:]
    mask = np.ones_like(hraw)
    for x in range(x_rho):
        index = np.where(hraw[:,x]<=0.5)
        mask[index,x] = 0
        h[index,x] = Tcline
    if smoother == 'Laplacian':
        from bathy_smoother.bathy_smoothing import smoothing_Laplacian_rx0
        h = smoothing_Laplacian_rx0(mask, hraw, rx0max)
    vgrid = pyroms.vgrid.s_coordinate(h, theta_b, theta_s, Tcline, N, hraw=hraw)

    # vgrid

    if geo:
        from mpl_toolkits.basemap import Basemap
        lat = np.linspace(lat[0], lat[1], y_rho+1)
        lon = np.linspace(lon[0], lon[1], x_rho+1)
        lon, lat = np.meshgrid(lon, lat)
        proj = Basemap(projection='merc', resolution=None, lat_ts=0.0)
        hgrid = pyroms.hgrid.CGrid_geo(lon, lat, proj)
    else:
        x, y = np.mgrid[0:(y_rho+1)*500:500, 0:(x_rho+1)*500:500]
        hgrid = pyroms.hgrid.CGrid(x, y)
    hgrid.mask[:,:] = mask
    hgrid.f = f

    # write

    grd = pyroms.grid.ROMS_Grid(name, hgrid, vgrid)
    pyroms.grid.write_ROMS_grid(grd, grdfile)

    # masklines

    if masklinesfile:
        import romspy
        romspy.add_masklines(grdfile, masklinesfile)


if __name__ == '__main__':

    grdfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-9.nc'
    meshfile = '/Users/teruhisa/Dropbox/Data/Grid/9/mesh-v5.csv'
    masklinesfile = '/Users/teruhisa/Dropbox/Data/masklines.csv'
    make_grd_file(grdfile, meshfile, masklinesfile)  # smoother=False

# coding: utf-8

import csv
import netCDF4


def _get_masklines(csvfile):

    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        lines = []
        for row in reader:
            if len(row) == 1:
                lines.append([[], []])
            else:
                lines[-1][0].append(int(row[0]))
                lines[-1][1].append(int(row[1]))
    return lines


def _add_maskline(nc, line):

    mask_u = nc.variables['mask_u']
    mask_v = nc.variables['mask_v']
    mask_psi = nc.variables['mask_psi']

    x = line[0]
    y = line[1]

    print len(x), x, y
    for i in xrange(len(x)-1):
        mask_psi[y[i], x[i]] = 0.0
        dx = x[i+1] - x[i]
        dy = y[i+1] - y[i]
        if dx == 1:
            mask_v[y[i], x[i]] = 0.0
        elif dx == -1:
            mask_v[y[i], x[i+1]] = 0.0
        elif dy == 1:
            mask_u[y[i], x[i]] = 0.0
        elif dy == -1:
            mask_u[y[i+1], x[i]] = 0.0

    return nc


def add_masklines(grdfile, linesfile):

    nc = netCDF4.Dataset(grdfile, 'r+')
    lines = _get_masklines(linesfile)
    for line in lines:
        nc = _add_maskline(nc, line)


if __name__ == '__main__':
    grdfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-9.0.nc'
    linfile = '/Users/teruhisa/Dropbox/Data/grid_mask_lines.csv'
    add_masklines(grdfile, linfile)

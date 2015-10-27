# coding: utf-8
# (c) 2015-10-21 Teruhisa Okada

import netCDF4
import numpy as np
from itertools import product
import pandas as pd
import datetime
try:
    from geopy.distance import vincenty
except:
    pass
import matplotlib.pyplot as plt

import romspy


def pickup(nc, vname, lon, lat, method='near'):

    lon_rho = nc.variables['lon_rho'][0,:]
    lat_rho = nc.variables['lat_rho'][:,0]

    d_lon = lon_rho - lon
    d_lat = lat_rho - lat
    x = abs(d_lon).argmin()
    y = abs(d_lat).argmin()

    if method == 'near':
        var = nc.variables[vname]
        if var.ndim == 4:
            return var[:,:,y,x]
        elif var.ndim == 3:
            return var[:,y,x]
        elif var.ndim == 2:
            return var[y,x]

    elif method == 'idw':
        s_lon = np.sign(d_lon[x])
        s_lat = np.sign(d_lat[y])
        if np.sign(d_lon[x+1]) != s_lon:
            x2 = [x, x+1]
        else:
            x2 = [x-1, x]
        if np.sign(d_lat[y+1]) != s_lat:
            y2 = [y, y+1]
        else:
            y2 = [y-1, y]
        var = nc.variables[vname]
        weight = np.zeros(4)
        var1 = [[] for _ in range(4)]
        for i, (x1, y1) in enumerate(product(x2, y2)):
            if nc.variables['mask_rho'][y1,x1] == 1:
                dx = x - x1
                dy = y - y1
                weight[i] = np.sqrt(abs(dx) ** 2 + abs(dy) ** 2)
                if var.ndim == 4:
                    var1[i] = var[:,:,y1,x1]
                if var.ndim == 3:
                    var1[i] = var[:,y1,x1]
                if var.ndim == 2:
                    var1[i] = var[y1,x1]
            else:
                weight[i] = 0
                var1[i] = 0
        return sum([var1[i] * weight[i] / sum(weight) for i in range(4)])

    else:
        print 'ERROR: your method "{}" is wrong'.format(method)

def test_pickup():
    nc = netCDF4.Dataset('Z:/roms/Apps/OB500_fennelP/NL12/ob500_avg.nc')
    var0 = pickup(nc, 'temp', 135.380822, 34.671375)
    var1 = pickup(nc, 'temp', 135.380822, 34.671375, 'idw')
    fig, ax = plt.subplots(2,1)
    p0 = ax[0].pcolor(var0.T)
    p1 = ax[1].pcolor(var1.T)
    #plt.colorbar(p0, ax=ax[0])
    plt.show()


def pickup_line(nc, vname, line, time, method='idw', cff=1.0, vmax=None, vmin=None):
    if type(time) == int:
        t = time
        time = netCDF4.num2date(nc.variables['ocean_time'][t], romspy.JST)
    elif type(time) == datetime.datetime:
        time2 = netCDF4.date2num(time, romspy.JST)
        time3 = nc.variables['ocean_time'][:]
        t = np.where(time3==time2)[0][0]
    else:
        print 'ERROR: your time type =',type(time)
    print '\n',time, t

    cs_r = nc.variables['Cs_r'][:]
    var = np.zeros([len(line),len(cs_r)])
    depth = np.zeros([len(line),len(cs_r)])
    dist = np.zeros([len(line),len(cs_r)])
    for s, l in enumerate(line):
        lon = l[0]
        lat = l[1]
        v = pickup(nc, vname, lon, lat, method)
        var[s,:] = v[t,:]
        h = pickup(nc, 'h', lon, lat, 'idw')
        try:
            zeta = pickup(nc, 'zeta', lon, lat, 'idw')
            depth[s,:] = (h + zeta[t]) * cs_r[:]
        except:
            depth[s,:] = (h + 1.0) * cs_r[:]
        if s == 0:
            dist[s,:] = 0
        else:
            back = line[s-1]
            fore = line[s]
            dist[s,:] = dist[s-1,:] + vincenty(back, fore).meters

    fig, ax = plt.subplots(figsize=[12,4])
    if (vmax is None) or (vmin is None):
        cflevels = romspy.vrange(vname, unit='g')
    else:
        cflevels = np.linspace(vmin, vmax, 21)
    clevels = cflevels
    origin = 'upper'
    #origin = 'lower'
    CF = plt.contourf(dist/1000, depth, var*cff, levels=cflevels, extend='both', origin=origin)
    C = plt.contour(dist/1000, depth, var*cff, colors='k', levels=clevels, origin=origin)
    plt.clabel(C, fmt='%2.1f', colors='w')
    #plt.pcolor(dist, depth, var) 　　　　　　　　　　# グリッド状がいいなら
    CB = plt.colorbar(CF)
    CB.ax.set_ylabel(vname)

    plt.xlabel('distance(km)')
    plt.ylabel('depth(m)')
    plt.title(datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S'))


def line_parser(linefile):
    df = pd.read_csv(linefile)
    return [[df.x[i], df.y[i]] for i in df.index]


def test_pickup_line():
    nc = netCDF4.Dataset('Z:/apps/OB500P/case13/ob500_avg.nc')
    line = line_parser('F:/okada/Dropbox/Data/stations_yodo.csv')
    #pickup_line(nc, 'temp', line, time=0, method='near')
    pickup_line(nc, 'salt', line, time=0, method='idw', vmin=0, vmax=32)
    plt.show()

if __name__ == '__main__':
    #test_pickup()
    test_pickup_line()
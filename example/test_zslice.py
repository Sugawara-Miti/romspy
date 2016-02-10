# coding: utf-8
# (c) 2016-02-10 Teruhisa Okada

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import romspy

inifile = '/home/okada/Data/ob500_ini_param6-ini_20120101.nc'
grdfile = '/home/okada/Data/ob500_grd-11_3.nc'

ini = netCDF4.Dataset(inifile, 'r')
grd = netCDF4.Dataset(grdfile, 'r')

h = grd['h'][:]
cs_r = grd['Cs_r'][:]
x_rho = grd['lon_rho'][0,:]
y_rho = grd['lat_rho'][:,0]
X, Y = np.meshgrid(x_rho, y_rho)

zeta = ini['zeta'][0,:,:]
temp = ini['temp'][0,:,:,:]
N, M, L = temp.shape

depth = np.zeros_like(temp)
for n in range(N):
    depth[n,:,:] = cs_r[n] * (zeta + h)

temp10 = romspy.zslice(temp, depth, -1)

fig, ax = plt.subplots(1,1,figsize=(6,5))
romspy.basemap()
C = ax.contourf(X, Y, temp10)
#C.label()
CB = plt.colorbar(C)
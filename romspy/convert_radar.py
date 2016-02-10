# coding: utf-8
# (c) 2015-12-04 Teruhisa Okada

import pandas as pd
import netCDF4
import romspy


def _plot(df):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,10))
    romspy.basemap()
    df2 = df['2012-08-01']
    ax = plt.gca()
    ax.quiver(df2.lon.values, df2.lat.values, df2.u.values, df2.v.values)
    plt.show()


def convert_radar(infile, outfile, gridfile, plot=False):
    names = ['date', 'xid', 'yid', 'lat', 'lon', 'u', 'v', 'dir', 'uv']
    df = pd.read_csv(infile, encoding='Shift_JIS', skiprows=1, names=names, index_col='date', parse_dates=['date'])

    grd = netCDF4.Dataset(grdfile, 'r')
    lon_rho = grd['lon_rho'][0,:]
    lat_rho = grd['lat_rho'][:,0]
    grd.close()

    dlon = (lon_rho[-1] - lon_rho[0]) / (len(lon_rho)-1)
    dlat = (lat_rho[-1] - lat_rho[0]) / (len(lat_rho)-1)
    lon2xgrid = lambda lon: (lon - lon_rho[0]) / dlon
    lat2ygrid = lambda lat: (lat - lat_rho[0]) / dlat
    df['xgrid'] = df.lon.apply(lon2xgrid)
    df['ygrid'] = df.lat.apply(lat2ygrid)

    if plot:
        _plot(df)

    df3 = df[['lat', 'lon', 'xgrid', 'ygrid']]
    df4 = df3[:]
    df3['value'] = df.u
    df3['type'] = 4
    df4['value'] = df.v
    df4['type'] = 5
    df3 = pd.concat([df3, df4], axis=0)
    df3.value = df3.value / 100.0

    df3.to_csv(outfile)

if __name__ == '__main__':

    infile = 'F:/okada/Data/radar/radar_20120201_20120301.csv'
    outfile = 'Z:/Data/radar/converted_radar_20120201_20120301.csv'
    grdfile = 'Z:/Data/ob500_grd-10.nc'
    #convert_radar(infile, outfile, grdfile, plot=True)
    convert_radar(infile, outfile, grdfile)

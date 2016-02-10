# coding: utf-8
# (c) 2015-11-04 Teruhisa Okada

import netCDF4
import pandas as pd
import romspy


def add_bioparam(inifile, csvfile):
    df = pd.read_csv(csvfile, index_col='name').T
    print df

    out = netCDF4.Dataset(inifile, 'a', format='NETCDF3_64BIT')

    try:
        out.createDimension('bioparam_time', 2)
        out.createDimension('Nbioparam', len(df.columns))
        time = out.createVariable('bioparam_time', 'f8', ('bioparam_time'))
        time.units = romspy.JST
    except:
        pass

    out.variables['bioparam_time'][0] = out.variables['ocean_time'][0]

    for name in df.columns.values:
        print name
        try:
            var = out.createVariable(name, 'f8', ('bioparam_time', 'Nbioparam'))
            var.units = df.units.values
            var.time = 'bioparam_time'
        except:
            pass
        out.variables[name][:,:] = df[name].values[0]

    out.close()

if __name__ == '__main__':
    Data = 'F:/okada/Dropbox/Data/'
    inifile = Data + 'ob500_ini_test.nc'
    csvfile = Data + 'bioparam.csv'
    add_bioparam(inifile, csvfile)

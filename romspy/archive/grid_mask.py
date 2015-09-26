# coding: utf-8

import netCDF4


def grid_mask(grdfile, reffile):

    grd = netCDF4.Dataset(grdfile, 'r+')
    ref = netCDF4.Dataset(reffile, 'r')

    mask_rho = grd.variables['mask_rho']
    mask_u = grd.variables['mask_u']
    mask_v = grd.variables['mask_v']
    mask_psi = grd.variables['mask_psi']

    masked_rho = ref.variables['mask_rho']
    masked_u = ref.variables['mask_u']
    masked_v = ref.variables['mask_v']
    masked_psi = ref.variables['mask_psi']

    mask_rho[:,:] = masked_rho[:,:]
    mask_u[:,:] = masked_u[:,:]
    mask_v[:,:] = masked_v[:,:]
    mask_psi[:,:] = masked_psi[:,:]

    grd.close()
    ref.close()

if __name__ == '__main__':

    grdfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-8-nomask.nc'
    reffile = '/Users/teruhisa/Dropbox/Data/ob500_grd-v3.1.nc'
    grid_mask(grdfile, reffile)

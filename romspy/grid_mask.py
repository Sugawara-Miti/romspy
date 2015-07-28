# coding: utf-8

import netCDF4

def grid_mask(editfile, editedfile):

    grid = netCDF4.Dataset(gridfile, 'r+')
    edited = netCDF4.Dataset(editedfile, 'r')

    mask_rho = grid.variables['mask_rho']
    mask_u = grid.variables['mask_u']
    mask_v = grid.variables['mask_v']
    mask_psi = grid.variables['mask_psi']

    masked_rho = edited.variables['mask_rho']
    masked_u = edited.variables['mask_u']
    masked_v = edited.variables['mask_v']
    masked_psi = edited.variables['mask_psi']

    mask_rho[:,:] = masked_rho[:,:]
    mask_u[:,:] = masked_u[:,:]
    mask_v[:,:] = masked_v[:,:]
    mask_psi[:,:] = masked_psi[:,:]

    edited.close()
    grid.close()

if __name__ == '__main__':

    gridfile = '/Users/teruhisa/Dropbox/matlab/ob500_grd.nc'
    editedfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-v5.nc'
    grid_mask(gridfile, editedfile)

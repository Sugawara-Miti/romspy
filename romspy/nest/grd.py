# -*- coding: utf-8 -*-

import netCDF4
import numpy as np
from numpy import dtype


def grid(oldfile, newfile, xi, eta):

    xi = np.arange(xi[0]-1, xi[1], 1)
    xi_u = xi[:-1]
    xi_v = xi[:]
    xi_psi = xi[:-1]
    eta = np.arange(eta[0]-1, eta[1], 1)
    eta_u = eta[:]
    eta_v = eta[:-1]
    eta_psi = eta[:-1]

    xi_rho = len(xi)
    eta_rho = len(eta)
    print xi_rho, xi
    print eta_rho, eta

    old = netCDF4.Dataset(oldfile, 'r')
    new = netCDF4.Dataset(newfile, 'w', format='NETCDF3_CLASSIC')

    new.createDimension("xi_rho", xi_rho)
    new.createDimension("xi_u", xi_rho-1)
    new.createDimension("xi_v", xi_rho)
    new.createDimension("xi_psi", xi_rho-1)

    new.createDimension("eta_rho", eta_rho)
    new.createDimension("eta_u", eta_rho)
    new.createDimension("eta_v", eta_rho-1)
    new.createDimension("eta_psi", eta_rho-1)

    spherical = new.createVariable('spherical', dtype('int32').char)
    xl = new.createVariable('xl', dtype('float32').char)
    el = new.createVariable('el', dtype('float32').char)
    h = new.createVariable('h', dtype('float32').char, ('eta_rho', 'xi_rho'))
    f = new.createVariable('f', dtype('float32').char, ('eta_rho', 'xi_rho'))
    pm = new.createVariable('pm', dtype('float32').char, ('eta_rho', 'xi_rho'))
    pn = new.createVariable('pn', dtype('float32').char, ('eta_rho', 'xi_rho'))

    spherical[:] = old.variables['spherical'][:]
    el[:] = 500.0 * xi_rho
    xl[:] = 500.0 * eta_rho
    h[:,:] = old.variables['h'][eta,xi]
    f[:,:] = old.variables['f'][eta,xi]
    pm[:,:] = old.variables['pm'][eta,xi]
    pn[:,:] = old.variables['pn'][eta,xi]

    xl.units = 'meter'
    el.units = 'meter'
    h.units = 'meter'
    f.units = 'second-1'
    pm.units = 'meter-1'
    pn.units = 'meter-1'

    names = ['x', 'y', 'lon', 'lat', 'mask']
    rho, u, v, psi = {}, {}, {}, {}

    for name in names:
        rho[name] = new.createVariable('{}_rho'.format(name), dtype('float32').char, ('eta_rho', 'xi_rho'))
        u[name]   = new.createVariable('{}_u'.format(name), dtype('float32').char, ('eta_u', 'xi_u'))
        v[name]   = new.createVariable('{}_v'.format(name), dtype('float32').char, ('eta_v', 'xi_v'))
        psi[name] = new.createVariable('{}_psi'.format(name), dtype('float32').char, ('eta_psi', 'xi_psi'))

        rho[name][:,:] = old.variables['{}_rho'.format(name)][eta, xi]
        u[name][:,:]   = old.variables['{}_u'.format(name)][eta_u, xi_u]
        v[name][:,:]   = old.variables['{}_v'.format(name)][eta_v, xi_v]
        psi[name][:,:] = old.variables['{}_psi'.format(name)][eta_psi, xi_psi]

        if name in ['x', 'y']:
            units = "meter"
        if name == 'lon':
            units = "degree_east"
        if name == 'lat':
            units = "degree_north"
        rho[name].units = units
        u[name].units   = units
        v[name].units   = units
        psi[name].units = units

    old.close()
    new.close()


if __name__ == '__main__':

    oldfile = '/Users/teruhisa/Dropbox/Data/ob500_grd-8-nomask.nc'
    newfile = '/Users/teruhisa/Dropbox/Data/ob500a_grd-8-nomask.nc'

    grid(oldfile, newfile, xi=[58,117], eta=[35,124])

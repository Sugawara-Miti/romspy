# coding: utf-8
# (C) 2014-2015 Teruhisa Okada
# This routine is based on pyroms.O2_saturation

import numpy as np

__version__ = 1.0

g2mol_O2 = 44.66 / 1.42903
mol2g_O2 = 1.42903 / 44.66


def O2_saturation(T,S):
    """
    Return saturation value of oxygen.

    Parameters
    ----------
    T : array_like
        Temperature (˚C)
    S : array_like
        Salinity (PSU)

    Returns
    -------
    O2_sat : array_like
        concentrations of O2 [ millimole O2 / m3 ] for a given temperature and
        salinity (at STP)
    """

    A1 = -173.4292
    A2 = 249.6339
    A3 = 143.3483
    A4 = -21.8492
    B1 = -0.033096
    B2 = 0.014259
    B3 = -0.0017000
    # Convert T to deg. C to deg. K
    T = T + 273.15
    # O2 Concentration in mg/l
    # [from Millero and Sohn, Chemical Oceanography, CRC Press, 1992]
    O = np.exp(A1 + A2*(100.0/T) + A3*np.log(T/100.0) + A4*(T/100.0) + 
               S*(B1 + B2*(T/100.0) + B3*((T/100.0)**2)))
    # Convert to mmol/m3
    #  mmol/m3 = 44.66 ml/l
    #  mg/l = ml/l * 1.42903 mg/ml
    return O / 1.42903 * 44.66


def DOsat_mol(T,S):
    return O2_saturation(T,S)


def DOsat_g(T,S):
    return O2_saturation(T,S) * mol2g_O2

if __name__ == '__main__':

    temp = np.asarray([10,20,25,25])
    salt = np.asarray([32,32,32,15])
    O2_g = np.asarray([3,3,3,3])
    O2_mol = O2_g * g2mol_O2
    O2sat_g = DOsat_g(temp, salt)
    O2sat_mol = O2sat_g * g2mol_O2
    print "O2    = {}(mg/l) = {}(mmol/m3)".format(O2_g, O2_mol)
    print "O2sat = {}(mg/l) = {}(mmol/m3)".format(O2sat_g, O2sat_mol)
    print "O2    = {}(%)".format(O2_g / O2sat_g * 100.0)

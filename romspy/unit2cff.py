# coding: utf-8
# (c) 2015-11-04 Teruhisa Okada

import romspy


def unit2cff(vname, unit):
    if 'g' in unit:
        if 'N' in vname:
            return romspy.mol2g_N
        elif 'P' in vname:
            return romspy.mol2g_P
        elif vname == 'oxygen':
            return romspy.mol2g_O2
        else:
            return 1.0
    else:
        return 1.0

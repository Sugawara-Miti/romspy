# coding: utf-8
# (c) 2015-10-21 Teruhisa Okada

import numpy as np
import romspy


def vrange(vname, unit='g'):
    vrange = {}
    vrange['temp'] = np.linspace(10, 30, 21)
    vrange['salt'] = np.linspace(23, 33, 21)
    vrange['NH4'] = np.linspace(0, 0.1, 21)
    vrange['NO3'] = np.linspace(0, 0.1, 21)
    vrange['chlorophyll'] = np.linspace(0, 20, 21)
    vrange['phytoplankton'] = np.linspace(0, 0.1, 21)
    vrange['zooplankton'] = np.linspace(0, 0.1, 21)
    vrange['LdetritusN'] = np.linspace(0, 0.1, 21)
    vrange['SdetritusN'] = np.linspace(0, 0.1, 21)
    vrange['oxygen'] = np.linspace(0, 10, 21)
    vrange['PO4'] = np.linspace(0, 0.005, 21)
    vrange['LdetritusP'] = np.linspace(0, 0.005, 21)
    vrange['SdetritusP'] = np.linspace(0, 0.005, 21)
    vrange['H2S'] = np.linspace(0, 0.1, 21)
    if 'g' in unit:
        return vrange[vname]
    elif 'mol' in unit:
        if 'N' in vname:
            return vrange[vname] * romspy.g2mol_N
        elif 'plankton' in vname:
            return vrange[vname] * romspy.g2mol_N
        elif 'P' in vname:
            return vrange[vname] * romspy.g2mol_P
        elif vname == 'oxygen':
            return vrange[vname] * romspy.g2mol_O2
        else:
            print 'ERROR:', vname, unit
    else:
        print 'ERROR:', vname, unit

if __name__ == '__main__':
    print vrange('oxygen', 'mol')
    print vrange('temp')
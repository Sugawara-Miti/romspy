# coding: utf-8
# (c) 2015-10-21 Teruhisa Okada

"""changelog
0.5 2015-11-04 rename vrange to levels
"""

import numpy as np
import romspy


def levels(vname, unit='g'):
    levels = {}
    levels['temp'] = np.arange(10, 30.1, 1)
    levels['salt'] = np.arange(15, 33.1, 1)
    levels['NH4'] = np.linspace(0, 0.5, 11)
    levels['NO3'] = levels['NH4']
    levels['chlorophyll'] = np.linspace(0, 20, 11)
    levels['phytoplankton'] = levels['NH4']
    levels['zooplankton'] = levels['NH4']
    levels['LdetritusN'] = levels['NH4']
    levels['SdetritusN'] = levels['NH4']
    levels['PO4'] = np.arange(0, 0.11, 0.01)
    levels['LdetritusP'] = levels['PO4']
    levels['SdetritusP'] = levels['PO4']
    levels['oxygen'] = np.arange(0, 10.1, 1)
    levels['H2S'] = np.arange(0, 0.101, 0.05)
    if vname not in levels.keys():
        return None
    elif 'g' in unit:
        return levels[vname]
    elif 'mol' in unit:
        if 'N' in vname:
            return levels[vname] * romspy.g2mol_N
        elif 'plankton' in vname:
            return levels[vname] * romspy.g2mol_N
        elif 'P' in vname:
            return levels[vname] * romspy.g2mol_P
        elif vname == 'oxygen':
            return levels[vname] * romspy.g2mol_O2
        else:
            print 'ERROR:', vname, unit
    else:
        print 'ERROR:', vname, unit

if __name__ == '__main__':
    print levels('oxygen', 'mol')
    print levels('temp')
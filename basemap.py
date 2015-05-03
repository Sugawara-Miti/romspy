# -*- coding: utf-8 -*-

"""
2015/05/01 okada updated this file.
"""

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.ticker import *
import matplotlib.pyplot as plt
import csv

def basemap(data='deg_OsakaBayMap_okada.bln'):
    
    """
    Title: Function of plotting map in Osaka Bay
    Created on 2014/07/17
    Referrence: http://matplotlib.org/examples/api/patch_collection.html
    """

    # Get land data 
    patches = _read_lands(data)

    # Plot patches
    p = PatchCollection(patches)#, alpha=0.5)
    p.set_facecolor('w')

    ax = plt.gca()
    
    ax.add_collection(p)

    # Set figure options
    ax.set_xlabel(u'Longitude [\N{DEGREE SIGN}E]')
    ax.set_ylabel(u'Latitude [\N{DEGREE SIGN}N]')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.set_xlim([134.82, 135.48])
    ax.set_ylim([ 34.20,  34.76])

def _read_lands(data):

    patches = []
    with open(data, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            row = row[0].split('\t')
            if '' in row:
                try: 
                    lands = Polygon(land, True)
                    patches.append(lands)
                except:
                    pass
                land = []
            else:
                land.append(map(float, row))
        lands = Polygon(land, True)
        patches.append(lands)
    return patches
    
if __name__=='__main__':

    basemap()
    plt.show()

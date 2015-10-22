# coding: utf-8
# (c) 2015-10-21 Teruhisa Okada

import matplotlib.pyplot as plt


def savefig(filename, dpi=300):
    plt.savefig(filename, bbox_inches='tight', dpi=dpi)

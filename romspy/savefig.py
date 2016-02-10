# coding: utf-8
# (c) 2015-10-21 Teruhisa Okada

import matplotlib.pyplot as plt


def savefig(figfile, dpi=300):
    plt.savefig(figfile, bbox_inches='tight', dpi=dpi)


if __name__ == '__main__':
    savefig('tplot.png')
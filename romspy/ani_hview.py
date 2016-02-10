# coding: utf-8
# (c) 2015-11-21 Teruhisa Okada

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import romspy

ncfile = 'Z:/apps/OB500P/case18/NL1/ob500_avg.nc'

nc = romspy.hview.Dataset(ncfile)
fig = plt.figure(figsize=[6,5])
im = []


def _update_hview(t, fig, im):
    if len(im) > 0:
        im[0].remove()
        im.pop()
    im.append(nc.hview('velocity', time=t))


ani = animation.FuncAnimation(fig, _update_hview, fargs=(fig, im), frames=6, interval=1)

plt.show()
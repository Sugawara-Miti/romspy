# coding: utf-8
# (c) 2015-12-09 Teruhisa Okada

import matplotlib.pyplot as plt
import seaborn as sns
import parse_mp

csvfile_tmp = 'F:/okada/Data/mp/mp_{0:03d}_A_20111231_20130101.csv'


def plot(tmpfile, station, layer):
    df = parse_mp.pickup(tmpfile, station, layer)
    plt.plot(df.light, df.chlo, '.', label='layer={}'.format(layer))
    plt.xlabel(u'light [μmol]')
    plt.xlim(-100, 1000)
    plt.ylabel('chlorophyll')
    plt.ylim(-20, 200)
    plt.title('Sta.{}'.format(station))
    plt.legend()


def plots(tmpfile, station):
    plot(station, 0.5)
    plot(station, 1.0)
    plot(station, 2.0)


def plots2(station):
    plot(station, 0.7)
    plot(station, 5.0)
    plot(station, 7.5)


def plot_osaka():
    plt.figure(figsize=(15,10))
    plt.subplot(2,3,1)
    plots(3)
    plt.subplot(2,3,2)
    plots(4)
    plt.subplot(2,3,3)
    plots2(5)
    plt.subplot(2,3,4)
    plots(6)
    plt.subplot(2,3,5)
    plots(12)
    plt.subplot(2,3,6)
    plots(13)

    import romspy
    plt.suptitle('osaka, 2012')
    romspy.savefig('F:/okada/Dropbox/Figures/analysis_mp/osaka2012_light_chlo.png')


if __name__ == '__main__':
    station = 4
    plot(csvfile_tmp, station, 0.5)
    plot(csvfile_tmp, station, 1.0)
    plot(csvfile_tmp, station, 5.0)
    plot(csvfile_tmp, station, 10.0)
    plt.show()
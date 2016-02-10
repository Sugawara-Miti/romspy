# coding: utf-8
# (c) 2015-10-14 Teruhisa Okada


def chl2phy(chl, C2Chl=0.0535):
    #flu2Chl = 2.18
    C = 12.00
    PhyCN = 16.0 / 106.0
    return chl / C2Chl / C * PhyCN

if __name__ == '__main__':
    print chl2phy(1.5)
    print chl2phy(1.5, 0.05)
    print chl2phy(1.5, 0.02)
    print chl2phy(0.5)
    print chl2phy(0.5, 0.05)
    print chl2phy(0.5, 0.02)

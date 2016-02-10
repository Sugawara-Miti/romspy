# coding: utf-8
# (c) 2015-10-14 Teruhisa Okada

C = 12.00            # g_C/mole_C
Chl2C_m = 0.0535     # mg_Chl/mg_C
PhyCN = 106.0/16.0   # mole_C/mole_N
a = 1.92             # mg_Chl(ship,model)/mg_Chl(obweb)
#flu2Chl = 2.18


def phy2chl(Chl2C=0.05):
    """
    return g_chl/mole_N
    2015-11-09 追加
    """
    return PhyCN * C * Chl2C


def chl2phy(chl, Chl2C=0.0535):
    """
    return mole_N
    """
    return chl / phy2chl(Chl2C)

if __name__ == '__main__':
    print 1/phy2chl()
    print phy2chl(Chl2C_m)

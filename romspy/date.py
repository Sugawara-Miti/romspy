# coding: utf-8

import netCDF4
import romspy


days_JST = 'days since 1968-05-23 09:00:00'
seconds_JST = 'seconds since 1968-05-23 09:00:00'


def mjd2date(mjd):
    return netCDF4.num2date(mjd, romspy.days_JST)


def mjs2date(mjs):
    return netCDF4.num2date(mjs, romspy.seconds_JST)

# coding: utf-8
# (c) 2015-2016 Teruhisa Okada

from add_masklines import add_masklines
from basemap import basemap
from c_his2ini import his2ini
from c_phy2chl import phy2chl
from cmap import cmap
from dataset import Dataset
from edit_nc_var import edit_nc_var
from get_time import get_time
from get_vnames import get_vnames
from initialize import initialize
from levels import levels
from O2_saturation import O2_saturation, DOsat_mol, DOsat_g, DOp2mol, DOp2g
from plot_cost import plot_cost
from pickup import pickup, pickup_line
from parsers import tide_parser, line_parser, date_parser
from read_mp import read_mp
from run_time import run_time
from savefig import savefig
from unit2cff import unit2cff

GMT = 'seconds since 1968-05-23 00:00:00 GMT'
JST = 'seconds since 1968-05-23 09:00:00 GMT'
GMT_days = 'days since 1968-05-23 00:00:00 GMT'
JST_days = 'days since 1968-05-23 09:00:00 GMT'

g2mol_C = 1000.0 / 12.00
g2mol_N = 1000.0 / 14.01
g2mol_P = 1000.0 / 30.97
mol2g_C = 12.00 / 1000.0
mol2g_N = 14.01 / 1000.0
mol2g_P = 30.97 / 1000.0

g2mol_O2 = 44.66 / 1.42903
mol2g_O2 = 1.42903 / 44.66

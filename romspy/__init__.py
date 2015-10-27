# coding: utf-8
# (c) 2015 Teruhisa Okada

__version__ = 0.0  # 2015-05-02
__version__ = 0.3  # 2015-10-22
__version__ = 0.4  # 2015-10-27

from make_ini_file import make_ini_file
from make_bry_file import make_bry_file
from make_frc_file import make_frc_file
from make_obs_file import make_obs_file
from make_river_file import make_river_file
from make_std_file import make_std_file
from make_grd_file import make_grd_file

from add_masklines import add_masklines

from basemap import basemap
#from hview import hview
import hview
from hview2 import hview2
from hplot_stations import hplot_stations
from hplot_values import hplot_values

from tview_obs import tview_obs

import profile
import profiles
import profiles_mg

from O2_saturation import O2_saturation, DOsat_mol, DOsat_g
from chl2phy import chl2phy
from vrange import vrange
from run_time import run_time
from pickup import pickup, pickup_line, line_parser
from savefig import savefig

from get_time import get_time
from get_vnames import get_vnames

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

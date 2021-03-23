#!/usr/bin/python3
"""
Convert data from CSV into NetCDF format,
including global and local attributes.
Attributes can be imported from .xls
"""

import os
import sys
import pathlib
from pathlib import Path
import pandas as pd
import numpy as np
import xarray as xr

from tools.container import Container
from tools.data import Data
from tools.xr import XR_Attrs

#%% DATA
data_path = Path('../data/mose/')
xls_file = 'test.xls'

data = pd.read_csv(data_path / 'MOSE1_TK3Result_Lindenberg.csv')
meta = pd.read_excel(data_path / xls_file,
                     sheet_name='csv2nc',
                     na_values=['NaN','n/a'])
global_attrs = pd.read_excel(data_path / xls_file,
                             sheet_name='global attributes',
                             na_values=['NaN','n/a'])

#%% MAIN

C = Container(meta)
target = C.target_df()

D = Data(data,target,
         time_index='T_mid',
         time_vars=['T_begin','T_end'])

dst = D.preprocessing()


incl_local = ['long_name', 'units', '_FillValue','ancillary_variables',
              'bounds', 'cell_methods', 'coordinates','comment', 'instrument']
incl_global = ['title','institution','source','history','references',
                'comment','campaign','featureType']

local_attrs = C.df

X = XR_Attrs(dst,
             local_attrs,
             incl_local,
             global_attrs,
             incl_global)

X.assign_global_attrs()
X.assign_local_attrs()


#%%


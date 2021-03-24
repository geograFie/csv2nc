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

from tools.container import DataContainer
from tools.data import Data
from tools.xr import XR_Attrs


#%% DATA
data_path = Path('../data/mose/')
xls_file = 'metadata.xls'

data = pd.read_csv(data_path / 'MOSE1_TK3Result_Lindenberg.csv')
meta = pd.read_excel(data_path / 'metadata.xls',
                     sheet_name='main', na_values=['NaN','nan','n/a'])

list_local_attrs = ['long_name', 'units', '_FillValue','ancillary_variables',
              'bounds', 'cell_methods', 'coordinates','comment', 'instrument']

global_attrs = pd.read_excel(data_path / xls_file,
                             sheet_name='global_attributes',
                             na_values=['NaN','nan','n/a'])

dims_attrs = pd.read_excel(data_path / xls_file,
                      sheet_name='dimensions',
                      na_values=['NaN','nan','n/a'])

DC = DataContainer(data,meta,global_attrs,dims_attrs,list_local_attrs)

#%% MAIN

da = Data(DC,time_index='T_mid',time_vars=['T_begin','T_end'])
dst = da.xr
X = XR_Attrs(dst,DC)
dst = X.assign_global_attrs()
dst = X.assign_local_attrs()
dst = X.expand_dims()
dst = X.assign_dim_attrs()

################# ????
# FLAGS
# ANCILLARY VARIABLES


#%%
dst = dst.chunk(chunks={'time':len(dst.time)})
dst.to_netcdf(data_path / 'MOSE_TK3_test.nc',
              unlimited_dims='time',
              mode='w', format='NETCDF4')
#%%


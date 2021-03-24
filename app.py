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

from tools.container import Metadata, DataContainer
from tools.data import Data
from tools.xr import XR_Attrs


#%% DATA
data_path = Path('../data/mose/')
xls_file = 'test.xls'

data = pd.read_csv(data_path / 'MOSE1_TK3Result_Lindenberg.csv')

metadata = pd.read_excel(data_path / xls_file,
                     sheet_name='csv2nc',
                     na_values=['NaN','nan','n/a'])

global_attrs = pd.read_excel(data_path / xls_file,
                             sheet_name='global attributes',
                             na_values=['NaN','nan','n/a'])

dims_attrs = pd.read_excel(data_path / xls_file,
                      sheet_name='coordinates',
                      na_values=['NaN','nan','n/a'])

DC = DataContainer(data=data,
                   metadata=metadata,
                   global_attrs=global_attrs,
                   dims_attrs=dims_attrs)


#%% MAIN

m = Metadata(DC)
target = m.target_df()

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
             incl_global,
             coords)

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


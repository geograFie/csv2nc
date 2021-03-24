#!/usr/bin/python3

import pandas as pd
import numpy as np
import xarray as xr

from .tools import Preprocessing

class XR_Attrs:
    def __init__(self, xr, local_attrs=None, incl_local=None,
                global_attrs=None, incl_global=None, coordinates=None):
        self.xr = xr
        self.data_vars = list(self.xr.data_vars)
        self.local_attrs = local_attrs
        self.global_attrs = global_attrs
        self.incl_local = incl_local
        self.incl_global = incl_global
        self.coords = self.df_pp(coordinates)

    def df_pp(self,df):
        df = df.copy()
        pp = Preprocessing(df)
        df = pp.strip_spaces(['standard_name','variable'])
        return df.set_index('variable')

    def assign_local_attrs(self):
        attributes = {var: {attr: self.local_attrs.loc[var,attr]
                            for attr in self.incl_local 
                            if self.local_attrs.loc[var,attr] is not np.nan}
                      for var in self.data_vars}

        # (i is np.nan) and (i == np.nan) are not equal expressions

        ######
        # if nan don't include
        ######

        for var in attributes:
            self.xr[var].attrs = attributes[var]

        return self.xr

    def assign_global_attrs(self):
        attributes = self.global_attrs.set_index('attribute')['example value'].to_dict()
        attributes = {key: attributes[key] for key in attributes
                      if attributes[key] is not np.nan}
        self.xr.attrs = attributes
        return self.xr

    def expand_dims(self):
        coordinates = self.coords['value'].to_dict()
        coordinates = {key: [coordinates[key]] for key in coordinates
                       if key not in self.xr.dims}

        # self.xr = self.xr.assign_coords(coordinates)

        self.xr = self.xr.expand_dims(coordinates)

        # dst = dst.assign_coords({'lat': 52.16418333,
        #                          'lon': 14.122222,
        #                          'alt': 73})
        return self.xr


    def assign_dim_attrs(self):
        for dim in list(self.xr.dims):
            attributes = self.coords.to_dict('index')[dim]
            attributes = {key: attributes[key] for key in attributes
                          if attributes[key] is not np.nan}
            self.xr[dim].attrs = attributes
        return self.xr
#!/usr/bin/python3

import pandas as pd
import numpy as np
import xarray as xr

from .container import DataContainer

class XR_Attrs:
    def __init__(self, xr, DataContainer):
        self.xr = xr
        self.DC = DataContainer
        self.data_vars = list(self.xr.data_vars)

    def assign_local_attrs(self):
        attributes = {var: {attr: self.DC.local_attrs.loc[var,attr]
                            for attr in list(self.DC.local_attrs)
                            if self.DC.local_attrs.loc[var,attr] is not np.nan}
                      for var in self.data_vars}

        for var in attributes:
            self.xr[var].attrs = attributes[var]
        return self.xr

    def assign_global_attrs(self):
        attributes = self.DC.global_attrs['value'].to_dict()
        attributes = {key: attributes[key] for key in attributes
                      if attributes[key] is not np.nan}
        self.xr.attrs = attributes
        return self.xr

    def expand_dims(self):
        dims = self.DC.dims_attrs['value'].to_dict()
        dims = {key: [dims[key]] for key in dims
                       if key not in self.xr.dims}
        self.xr = self.xr.expand_dims(dims)
        return self.xr

    def assign_dim_attrs(self):
        for dim in list(self.xr.dims):
            attributes = self.DC.dims_attrs.to_dict('index')[dim]
            attributes = {key: attributes[key] for key in attributes
                          if attributes[key] is not np.nan}
            self.xr[dim].attrs = attributes
        return self.xr




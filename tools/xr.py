#!/usr/bin/python3

import pandas as pd
import numpy as np
import xarray as xr

class XR_Attrs:
    def __init__(self, xr, local_attrs, incl_local, global_attrs, incl_global):
        self.xr = xr
        self.data_vars = list(self.xr.data_vars)
        self.local_attrs = local_attrs
        self.global_attrs = global_attrs
        self.incl_local = incl_local
        self.incl_global = incl_global

    def assign_local_attrs(self):
        attributes = {var: {attr: self.local_attrs.loc[var, attr]
                            for attr in self.incl_local} for var in self.data_vars}

        ######
        # if nan don't include
        ######

        for var in attributes:
            self.xr[var].attrs = attributes[var]

        return self.xr

    def assign_global_attrs(self):
        self.xr.attrs = self.global_attrs.set_index('attribute')['example value'].to_dict()
        return self.xr
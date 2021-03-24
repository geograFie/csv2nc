#!/usr/bin/python3

import pandas as pd
import numpy as np

class Preprocessing:
    def __init__(self,df):
        self.df = df

    def strip_spaces(self, varnames):
        print('removing spaces')
        """remove leading and trailing spaces"""
        self.df = self.df.copy()  # not necessary but to prevent CopyWarning
        # tmp = self.df.select_dtypes(['object'])
        self.df.loc[:, varnames] = self.df[varnames].apply(lambda x: x.str.strip())
        return self.df


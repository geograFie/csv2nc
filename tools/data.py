#!/usr/bin/python3

import pandas as pd
import xarray as xr

from .container import DataContainer

class Data:
    def __init__(self, DataContainer,time_index='T_mid',
                 time_vars=None, seconds_since='1970-01-01'):  # , set_index=['T_mid']):
        self.DC = DataContainer
        self.time_vars = time_vars
        self.since = str(seconds_since)
        self.time_index = time_index
        self.xr = self.df2xr()

    def time(self):
        def seconds_since(df):
            df = pd.to_datetime(df)
            return pd.Series(df - pd.Timestamp(self.since)).dt.total_seconds()

        time = pd.DataFrame()
        if self.time_index in list(self.DC.data.columns):
            time['time'] = seconds_since(self.DC.data[self.time_index])
        else:
            if self.time_vars == None:
                raise ValueError('{} not a column in dataset.\
                 Please give column names ("time_vars") from which to calculate the mid time.'.format(
                    self.time_index))
            else:
                time['begin'] = pd.to_datetime(self.DC.data[self.time_vars[0]])
                time['end'] = pd.to_datetime(self.DC.data[self.time_vars[1]])
                time['period_mid'] = time['begin'] + (time['end'] - time['begin']) / 2
                time['time'] = seconds_since(time['period_mid'])
        return time[['time']]


    def df2xr(self):
        df = self.DC.data[self.DC.src_names].copy()
        df[self.time_index] = self.time()
        df = df.rename(columns=self.DC.nc_rename)
        df = df.set_index(self.DC.nc_rename[self.time_index])
        return df.to_xarray()

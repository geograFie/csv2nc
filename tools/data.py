#!/usr/bin/python3

import pandas as pd
import xarray as xr

class Data:
    def __init__(self, df, conversion,
                 time_index='T_mid', time_vars=None, seconds_since='1970-01-01'):  # , set_index=['T_mid']):
        self.conv = conversion
        self.src_names = list(self.conv['src_name'])
        self.dst_names = list(self.conv.index)
        self.rename = {src: dst for src, dst in zip(self.src_names, self.dst_names)}
        #         self.rename = self.conv['rename'].to_dict()
        self.df = df
        self._FillValue = self.conv['_FillValue']
        self.time_index = time_index
        self.time_vars = time_vars
        self.since = str(seconds_since)

    def time(self):
        def seconds_since(df):
            df = pd.to_datetime(df)
            return pd.Series(df - pd.Timestamp(self.since)).dt.total_seconds()

        time = pd.DataFrame()
        if self.time_index in list(self.df.columns):
            time['time'] = seconds_since(self.df[self.time_index])
        else:
            time['begin'] = pd.to_datetime(self.df[self.time_vars[0]])
            time['end'] = pd.to_datetime(self.df[self.time_vars[1]])
            time['period_mid'] = time['begin'] + (time['end'] - time['begin']) / 2
            time['time'] = seconds_since(time['period_mid'])

        return time[['time']]

    def preprocessing(self):
        df = self.df[self.src_names].copy()
        df[self.time_index] = self.time()
        df = df.rename(columns=self.rename)
        df = df.set_index(self.rename[self.time_index])

        #         NaNs ????????

        return df.to_xarray()
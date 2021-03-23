#!/usr/bin/python3

import pandas as pd
import numpy as np


class Container:
    def __init__(self, df):
        self.df = df[df['standard_name'].isnull() == False].set_index('standard_name')
        self.src_names = list(self.df['src_name'])
        self.dst_names = list(self.df.index)
        self.unit_conv = list(self.df['unit_conversion'].replace({np.nan: '*1'}))
        self._FillValue = list(self.df['_FillValue'])

    #         test.T.set_index('standard_name').T

    #         self.src_names = list(self.df.loc['src_name'])
    #         self.dst_names = list(self.df.loc['standard_name'])
    #         self.unit_conv = list(self.df.loc['unit_conversion'].replace({np.nan:'*1'}))
    #         self._FillValue = list(self.df.loc['_FillValue'])
    #         self.local_attrs = local_attrs
    #         self.dst_df = self.target_df()

    #         df.loc['src_name'] = list(df.columns)
    #         #df.loc['src_name'] = list(df.columns)
    #         #df = df.set_index('standard_name')

    #         return df

    def unit_conversion(self):

        def check_operators(x):
            try:
                return '%+g' % float(x)
            except:
                if str(x)[0] not in ['/', '*', '-', '+']:
                    return '*1'
                else:
                    return x

        conv = {k: check_operators(v) for k, v in zip(self.src_names, self.unit_conv)}
        return conv

    def names(self):  # better: rename
        return {src: dst for src, dst in zip(self.src_names, self.dst_names)}

    #     def remove space at beginning or end of a key

    def check_dupl(self):
        """Check for duplicates in standard_name column"""
        vals, counts = np.unique(list(self.names().values()), return_counts=True)
        if len(vals) != len(self.names().values()):
            doubles = [k for k in self.names() if self.names()[k] in vals[counts > 1]]
            raise ValueError(
                'Duplicates detected! Please check again the standard_name of following variables: {}'.format(doubles))
        else:
            pass

    def target_df(self):
        self.check_dupl()

        dst = pd.DataFrame(zip(self.src_names,
                               self.unit_conversion().values()),
                           index=self.dst_names,
                           columns=['src_name', 'conv_factor'])
        dst['unit_conversion'] = dst.index + dst['conv_factor']
        dst['_FillValue'] = self._FillValue

        #         for i in self.local_attrs:
        #             dst[i] = self.df.loc[i]

        #         return self.df[list(self.names())]
        return dst

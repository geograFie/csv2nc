#!/usr/bin/python3

import pandas as pd
import numpy as np

def strip_spaces(df, varnames):
    """remove leading and trailing spaces"""
    df = df.copy()  # not necessary but to prevent CopyWarning
    # tmp = self.df.select_dtypes(['object'])
    df.loc[:, varnames] = df[varnames].apply(lambda x: x.str.strip())
    return df



class DataContainer:
    def __init__(self,data,metadata,global_attrs,dims_attrs, list_local_attrs):
        self.data = data
        self.metadata = self.pp(metadata)

        self.src_names = list(self.metadata['src_name'])
        self.dst_names = list(self.metadata.index)
        self.std_names = list(self.metadata['standard_name'])
        self.lng_names = list(self.metadata['long_name'])
        self.nc_rename = self.rename()

        # df = df[df['standard_name'].isnull() == False]
        self.global_attrs = global_attrs.set_index('attribute')
        self.list_local_attrs = list_local_attrs
        self.local_attrs = self.metadata[self.list_local_attrs]
        self.dims_attrs = strip_spaces(
            dims_attrs,['standard_name','variable']).set_index('variable')
        self.dims = list(self.dims_attrs.index)

        self.unit_conv = self.unit_conversion()

    def pp(self,df):
        """preprocessing:
        select variables only where conver2nc is marked True,
        remove accidental leading or trailing spaces.
        """
        df = df[df.loc[:,'convert2nc'] == True]
        df = strip_spaces(df,['standard_name', 'src_name','variable'])
        return df.set_index('variable')

    def rename(self):
        """Check if target list of variable names contains missing names or
        duplicates. If not, return source and destination names as dict.
        """
        # Check for missing names in dst_names
        if np.nan in self.dst_names:
            a = [self.src_names[i] for i,dst in enumerate(self.dst_names)
                 if dst is np.nan]
            raise ValueError('Variable(s) without target name(s) detected. Please assign {} a name.'.format(a))

        # Check for duplicates in dst_names
        elif len(set(self.dst_names)) < len(self.dst_names):
            vals, counts = np.unique(self.dst_names, return_counts=True)
            a = [vals[i] for i,c in enumerate(counts) if c > 1]
            raise ValueError('Duplicates detected! {} appears more often than once.'.format(a))

        else:
            return {src: dst for src, dst in zip(self.src_names, self.dst_names)}

    def unit_conversion(self):
        def check_operators(x):
            try:
                return '%+g' % float(x)
            except:
                if str(x)[0] not in ['/', '*', '-', '+']:
                    return '*1'
                else:
                    return x

        conv_list = list(self.metadata['unit_conversion'].replace({np.nan: '*1'}))
        unit_conv = {dst: dst + check_operators(conv)
                for dst, conv in zip(self.dst_names, conv_list)}
        return unit_conv


# class Metadata:
#     def __init__(self, DataContainer):
#         self.DC = DataContainer
#         self.src_names = self.DC.src_names
#         self.dst_names = self.DC.dst_names
#         self.metadata = self.DC.metadata
#
#         self.unit_conv = self.unit_conversion()
#         self._FillValue = list(self.metadata['_FillValue'])


    # def unit_conversion(self):
    #     def check_operators(x):
    #         try:
    #             return '%+g' % float(x)
    #         except:
    #             if str(x)[0] not in ['/', '*', '-', '+']:
    #                 return '*1'
    #             else:
    #                 return x
    #
    #     conv_list = list(self.metadata['unit_conversion'].replace({np.nan: '*1'}))
    #     unit_conv = {dst: dst + check_operators(conv)
    #             for dst, conv in zip(self.dst_names, conv_list)}
    #     return unit_conv

    # def target_df(self):
    #     self.check_dupl()
    #
    #     dst = pd.DataFrame(zip(self.src_names,
    #                            self.unit_conversion().values()),
    #                        index=self.dst_names,
    #                        columns=['src_name', 'conv_factor'])
    #     dst['unit_conversion'] = dst.index + dst['conv_factor']
    #     dst['_FillValue'] = self._FillValue
    #
    #             for i in self.local_attrs:
    #                 dst[i] = self.df.loc[i]
    #
    #             return self.df[list(self.names())]
    #     return dst

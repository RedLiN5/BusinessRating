#!/usr/bin/python
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import sys
import re
reload(sys)
import scipy 

class Preprocessing(object):

    def __init__(self, file, sep = ',', header = 0, index_col = 0):
        self.file = file
        self.sep = sep
        self.header = header
        self.index_col = index_col

    def ReadData(self):
        self.data = pd.read_table(self.file, sep = self.sep, header = self.header,
                             index_col = self.index_col)

    def DropFeatureNA(self, dataframe, MainFeatures):
        temp_df = dataframe[MainFeatures]
        na_index = temp_df.isnull().T.any()
        temp_df = temp_df[~na_index]
        return temp_df

    def RegFilter(self, x):
        pattern1 = r'.*轮'
        pattern2 = r'IPO.*'
        regexp1 = re.compile(pattern1)
        regexp2 = re.compile(pattern2)

        if regexp1.search(x) or regexp2.search(x) is not None:
            return True
        else:
            return False

    def preprocess(self):
        self.ReadData()
        df = self.data

        if sum(df.isnull().any()) == 0:
            pass
        else:
            df = self.DropFeatureNA(df, ['Investor', 'Investee', 'FinancingRound'])

        filter_index = np.array(map(self.RegFilter, df['FinancingRound']))
        df = df[filter_index]
        return df



#!/usr/bin/python
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import sys
import re
reload(sys)

class Preprocessing(object):

    def __init__(self, file, sep = ',', header = 0, index_col = 0):
        self.file = file
        self.sep = sep
        self.header = header
        self.index_col = index_col

    def read_data(self):
        self.data = pd.read_table(self.file, sep = self.sep, header = self.header,
                             index_col = self.index_col)

    def drop_feature_na(self, dataframe, MainFeatures):
        temp_df = dataframe[MainFeatures]
        na_index = temp_df.isnull().T.any()
        temp_df = temp_df[~na_index]
        return temp_df

    def reg_filter(self, x):
        pattern1 = r'.*轮'
        pattern2 = r'IPO.*'
        regexp1 = re.compile(pattern1)
        regexp2 = re.compile(pattern2)

        if regexp1.search(x) or regexp2.search(x) is not None:
            return True
        else:
            return False

    def replace(self, x):
        x = re.sub(r'轮', '', x)
        if x == r'IPO上市后':
            return 'afterIPO'
        elif x == r'IPO上市':
            return 'IPO'
        elif x == r'F-上市前':
            return 'FbeforeIPO'
        elif x == 'B+':
            return 'Bplus'
        elif x == 'Pre-B':
            return 'preB'
        elif x == 'A+':
            return 'Aplus'
        elif x == 'Pre-A':
            return 'preA'
        elif x == r'天使':
            return 'Angel'
        elif x == r'种子':
            return 'Seed'
        else:
            return x

    def fit(self):
        self.read_data()
        df = self.data

        if sum(df.isnull().any()) == 0:
            pass
        else:
            df = self.drop_feature_na(df, ['Investor', 'Investee', 'FinancingRound'])

        filter_index = np.array(map(self.reg_filter, df['FinancingRound']))
        df = df[filter_index]
        df['FinancingRound'] = map(self.replace, df['FinancingRound'])
        return self.df




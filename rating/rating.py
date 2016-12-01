from etl import Preprocessing
import numpy as np
import pandas as pd



class GetScore(Preprocessing):

    def __init__(self, name):
        self.name = name

    def preprocess(self):
        pre = Preprocessing('../data/mydata.csv')
        pre.fit()

    def search(self):
        df = self.df
        target_index = df['Investee'] == self.name
        if sum(target_index) > 1:
            investors = df[target_index]
        elif sum(target_index) == 1:
            round, amount = df.ix[target_index, ['FinancingRound', 'Amount']]
            

###############

pre = Preprocessing('../data/mydata.csv')
df = pre.fit()

print len(np.unique(df['Investee']))
print df.columns, df.shape
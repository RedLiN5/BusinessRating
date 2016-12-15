# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys

sys.path.append('..')
from rating.InvestorRating import InvestorScore

class DataNormalization(InvestorScore):

    def __init__(self):
        super(DataNormalization, self).__init__()
        self.fit()

    def normalization(self):
        df = self.df.copy()
        investors_unique = np.unique(df['Investor'].values)
        scores = list(map(self.investor_score, investors_unique))
        df_unique = pd.DataFrame({'Investor': investors_unique, 'Score': scores})
        df_new = df_unique.loc[df_unique.Score != -1]
        scores_new = df_new.Score
        scores_normal = (scores_new - np.mean(scores_new))/(max(scores_new) - min(scores_new))
        scores_normal = scores_normal + abs(min(scores_normal))
        df_new.Score = scores_normal
        self.normal_score = df_new

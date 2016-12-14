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

    def normal(self):
        df = self.df.copy()
        investors_unique = np.unique(df['Investor'].values)
        scores = list(map(self.investor_score, investors_unique))
        scores_normal = (scores - np.mean(scores))/(max(scores) - min(scores))
        investor_score = pd.DataFrame({'Investor': investors_unique, 'Score': scores_normal})
        return investor_score
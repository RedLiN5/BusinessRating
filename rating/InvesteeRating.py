# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import sys
sys.path.append('..')

from rating.InvestorRating import InvestorScore
from rating.etl import Preprocessing
from data.Normalization import DataNormalization

class InvesteeScore(DataNormalization):

    def __init__(self, investee):
        self.investee = investee
        Preprocessing.__init__(self, file='data/mydata.csv', sep = ',', header = 0, index_col = 0)
        self.fit()
        DataNormalization.__init__(self)
        self.normalization()

    def investee_final_score(self):
        df = self.df
        investee_ind = df.Investee == self.investee
        investee_investors = df.ix[investee_ind, 'Investor'].values
        normal_score = self.normal_score

        scores = []
        n = 0
        for investor in investee_investors:
            try:
                investor in normal_score.Investor
                investor_ind = normal_score.Investor == investor
                score = normal_score.ix[investor_ind, 'Score'].values[0]
                scores.append(score)
                n = n + 1
            except:
                print('Investor %s info cannot currently be obtained.'% investor)

        score_mean = sum(scores)/float(n)
        return score_mean
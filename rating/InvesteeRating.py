# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from InvestorRating import InvestorScore
from etl import Preprocessing

class InvesteeScore(InvestorScore, Preprocessing):

    def __init__(self, investee):
        self.investee = investee
        InvestorScore.__init__(self)
        Preprocessing.__init__(self, file='../data/mydata.csv', sep = ',', header = 0, index_col = 0)
        self.fit()

    def investee_final_score(self):
        df = self.df
        investee_ind = df.Investee == self.investee
        investee_investors = df.ix[investee_ind, 'Investor'].values

        scores = []
        n = 0
        for investor in investee_investors:
            score = self.investor_score(investor=investor)
            if isinstance(score, str):
                continue
            else:
                n += 1
                scores += [score]
        score_mean = sum(scores)/float(n)
        return score_mean
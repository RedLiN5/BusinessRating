# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from etl import Preprocessing

class InvestorScore(Preprocessing):

    def __init__(self, investor):
        self.investor = investor
        super(InvestorScore,self).__init__(file='../data/mydata.csv', sep = ',', header = 0, index_col = 0)
        self.fit()

    def generate_table(self):
        table = dict(
            Seed  = dict(Angel=0, preA=.1, A=.2, Aplus=.25, preB=.3, B=.4, Bplus=.45,
                         C=.6, D=.75, E=.85, FbeforeIPO=.95, IPO=1, afterIPO=1),
            Angel = dict(Seed=0, preA=.1, A=.2, Aplus=.25, preB=.3, B=.4, Bplus=.45,
                         C=.6, D=.75, E=.85, FbeforeIPO=.95, IPO=1, afterIPO=1),
            preA  = dict(A=.1, Aplus=.2, preB=.25, B=.3, Bplus=.4, C=.45, D=.6,
                         E=.75, FbeforeIPO=.85, IPO=.95, afterIPO=.95),
            A     = dict(Aplus=.1, preB=.2, B=.25, Bplus=.3, C=.4, D=.45, E=.6,
                         FbeforeIPO=.75, IPO=.85, afterIPO=.85),
            Aplus = dict(preB=.1, B=.2, Bplus=.25, C=.3, D=.4, E=.45, FbeforeIPO=.6,
                         IPO=.75, afterIPO=.75),
            preB  = dict(B=.1, Bplus=.2, C=.25, D=.3, E=.4, FbeforeIPO=.45,
                         IPO=.6, afterIPO=.6),
            B     = dict(Bplus=.1, C=.2, D=.25, E=.3, FbeforeIPO=.4, IPO=.45,
                         afterIPO=.45),
            Bplus = dict(C=.1, D=.2, E=.25, FbeforeIPO=3, IPO=.4, afterIPO=.4),
            C     = dict(D=.1, E=.2, FbeforeIPO=.25, IPO=.3, afterIPO=.3),
            D     = dict(E=.1, FbeforeIPO=.2, IPO=.25, afterIPO=.25),
            E     = dict(FbeforeIPO=.1, IPO=.2, afterIPO=.2),
            FbeforeIPO = dict(IPO=.1, afterIPO=.1),
            IPO   = dict(afterIPO=.05)
        )
        return table

    def calculator(self, round_in, round_now):
        table_dict = self.generate_table()
        score = table_dict[round_in][round_now]
        return score

    def get_score(self, investor, investee):
        investee_df = self.df[self.df['Investee'] == investee]
        rounds = investee_df['FinancingRound']
        invstr_ind = investee_df['Investor'] == investor
        print(invstr_ind)
        round_in = investee_df.ix[invstr_ind, 'FinancingRound'].values[0]
        # Round in is a map object
        print('round in:', round_in)
        if 'afterIPO' in rounds:
            round_now = 'afterIPO'
        elif 'IPO' in rounds:
            round_now = 'IPO'
        elif 'FbeforeIPO' in rounds:
            round_now = 'FbeforeIPO'
        elif 'E' in rounds:
            round_now = 'E'
        elif 'D' in rounds:
            round_now = 'D'
        elif 'C' in rounds:
            round_now = 'C'
        elif 'Bplus' in rounds:
            round_now = 'Bplus'
        elif 'B' in rounds:
            round_now = 'B'
        elif 'preB' in rounds:
            round_now = 'preB'
        elif 'Aplus' in rounds:
            round_now = 'Aplus'
        elif 'A' in rounds:
            round_now = 'A'
        elif 'preA' in rounds:
            round_now = 'preA'
        else:
            round_now = 'Angel'

        score = self.calculator(round_in=round_in, round_now=round_now)
        return score

    def start(self):
        investor_ind = self.df['Investor'] == self.investor
        print(sum(investor_ind))
        investees = self.df.ix[investor_ind, 'Investee']
        n = len(investees)
        print(investees)
        scores = []
        for investee in investees.values:
            scores += [self.get_score(investor=self.investor, investee=investee)]
        # return sum(scores)/float(n)
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

class InvestorScore(object):

    def __int__(self, investor, df):
        self.df = df
        self.investor = investor
        self.rounds_sort = ['IPO上市后','IPO上市','F轮-上市前','E轮','D轮','C轮','B+轮',
                            'B轮','Pre-B轮','A+轮','A轮','Pre-A轮','天使轮','种子轮']

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



    def get_score(self, investor, investee):
        investee_df = self.df[self.df['Investee'] == investee]
        rounds = investee_df['FinancingRound']
        round_in = investee_df.ix[investee_df['Investor'] == investor, 'FinancingRound']



    def start(self):
        investor_ind = self.df['Investor'] == self.investor
        investees = self.df.ix[investor_ind, 'Investee']
        for investee in investees:
            self.get_score(investor=self.investor, investee=investee)
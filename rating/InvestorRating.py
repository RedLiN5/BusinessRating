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
        self.table = dict(
            Seed = dict(Angel=0, preA=.1, A=.2, Aplus=.25, preB=.3, B=.4, Bplus=.45,
                        C=.6, D=.75, E=.85, FbeforeIPO=.95, IPO=1, afterIPO=1),
            Angel = dict(Seed=0, preA=.1, A=.2, Aplus=.25, preB=.3, B=.4, Bplus=.45,
                        C=.6, D=.75, E=.85, FbeforeIPO=.95, IPO=1, afterIPO=1),
            preA = dict(A=.1, Aplus=.2, preB=.25, B=.3, Bplus=.4, C=.45, D=.6,
                        E=.75, FbeforeIPO=.85, IPO=.95, afterIPO=.95)

        )

    def calculator(self, round_in, round_now):
        pass


    def get_score(self, investor, investee):
        investee_df = self.df[self.df['Investee'] == investee]
        rounds = investee_df['FinancingRound']
        round_in = investee_df.ix[investee_df['Investor'] == investor, 'FinancingRound']



    def start(self):
        investor_ind = self.df['Investor'] == self.investor
        investees = self.df.ix[investor_ind, 'Investee']
        for investee in investees:
            self.get_score(investor=self.investor, investee=investee)
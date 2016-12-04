import numpy as np
import pandas as pd

class InvestorScore(object):

    def __int__(self, investor, df):
        self.df = df
        self.investor = investor
        self.rounds_sort = ['IPO上市后','IPO上市','F轮-上市前','E轮','D轮','C轮','B+轮',
                            'B轮','Pre-B轮','A+轮','A轮','Pre-A轮','天使轮','种子轮']

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
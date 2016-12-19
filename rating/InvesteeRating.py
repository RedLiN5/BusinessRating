# -*- coding: utf-8 -*-
"""
NAME
    InvesteeRating

DESCRIPTION
    This module only includes the method to calculate an investee's score

CLASS
    InvesteeRating.InvesteeScore

"""

from rating.etl import Preprocessing
from data.Normalization import DataNormalization

class InvesteeScore(DataNormalization):
    """
    Calculate an investee's score based on one's investors' ratings.

    Parameters
    ----------
    investee: str
    """
    def __init__(self, investee):
        self.investee = investee
        Preprocessing.__init__(self,
                               file='data/mydata.csv',
                               sep=',',
                               header=0,
                               index_col=0)
        self.fit()
        DataNormalization.__init__(self)
        self.normalization()

    def investee_final_score(self):
        """
        Calculate an investee score.

        Returns
        -------
        score_mean: int
        """
        data_df = self.df
        investee_ind = data_df.Investee == self.investee
        investee_investors = data_df.ix[investee_ind, 'Investor'].values
        normal_score = self.normal_score

        scores = []
        n_scores = 0
        for investor in investee_investors:
            try:
                while investor in normal_score.Investor:
                    investor_ind = normal_score.Investor == investor
                    score = normal_score.ix[investor_ind, 'Score'].values[0]
                    scores.append(score)
                    n_scores = n_scores + 1
            except:
                print('Investor %s info cannot currently be obtained.'% investor)

        try:
            score_mean = sum(scores)/float(n_scores)
            return score_mean
        except Exception as error:
            print('Investor %s info cannot currently be obtained, because of %s' % (investor, error))
            
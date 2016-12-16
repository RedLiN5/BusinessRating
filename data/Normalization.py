# -*- coding: utf-8 -*-
"""
NAME
    normalization

DESCRIPTION
    =====

    Provides
      Normalization for investor scores.

"""

import math
import pandas as pd
import numpy as np
from rating.InvestorRating import InvestorScore


class DataNormalization(InvestorScore):
    """
    Methods defined here:

    normalization(self)
        Process if data frame from InvestorScore exists.
    """

    def __init__(self):
        super(DataNormalization, self).__init__()
        self.fit()
        self.normal_score = None

    def normalization(self):
        """
        normalization(...)

        Run normalization process.
        :return:
        """
        dataframe = self.df.copy()
        investors_unique = np.unique(dataframe['Investor'].values)
        scores = list(map(self.investor_score, investors_unique))
        df_unique = pd.DataFrame({'Investor': investors_unique, 'Score': scores})
        df_new = df_unique.loc[df_unique.Score != -1]
        scores_new = df_new.Score
        scores_mean = np.mean(scores_new)
        scores_std = np.std(scores_new)
        scores_length = len(scores_new)
        scores_normal = (scores_new - scores_mean)/(scores_std/math.sqrt(scores_length))
        scores_normal = scores_normal + 0.5
        df_new.Score = scores_normal
        self.normal_score = df_new

#!/usr/bin/python
# -*- coding: utf-8 -*-

from InvestorRating import InvestorScore
from etl import Preprocessing
import numpy as np
import pandas as pd


class GetScore(InvestorScore):

    def __init__(self, name):
        super(GetScore,self).__init__(investor=name)

    def return_score(self):
        return self.start()


test = GetScore(name = '立元创投')
print(test.return_score())

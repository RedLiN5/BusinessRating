#!/usr/bin/python
# -*- coding: utf-8 -*-

from InvestorRating import InvestorScore
from etl import Preprocessing
import numpy as np
import pandas as pd
from InvesteeRating import InvesteeScore


class Score(InvesteeScore):

    def __init__(self, name):
        self.name = name
        super(Score, self).__init__(investee = name)

    def calculate(self):
        return self.investee_final_score()


test = Score(name = '滴滴出行-滴滴快的')
print(test.calculate())

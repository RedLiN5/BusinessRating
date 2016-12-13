import pandas as pd
import numpy as np
from ..rating.etl import Preprocessing

class DataNormalization(Preprocessing):

    def __init__(self):
        super(DataNormalization, self).__init__(file='mydata.csv')
        self.fit()


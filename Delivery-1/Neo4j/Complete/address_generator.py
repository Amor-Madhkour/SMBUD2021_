# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 13:10:34 2021

@author: matteo
"""

import pandas as pd
import numpy as np


class AddressGeenerator:
    MAX_ADDRESS_NUMBER = 30
    
    def __init__(self):
        self.city_names = np.array(pd.read_csv("cities.csv").iloc[:,0])
        self.street_names = np.array(pd.read_csv("streets.csv").iloc[:,0])
    
    def get_address(self):
        city = self.city_names[np.random.randint(0,len(self.city_names))]
        street = self.street_names[np.random.randint(0,len(self.street_names))]
        number = np.random.randint(1,self.MAX_ADDRESS_NUMBER+1)
        return (street+str(number),city)




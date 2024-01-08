# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 18:11:49 2021

@author: matteo
"""

import numpy as np
import pandas as pd

class AuthBody:
    
    
    DEPARTMENTS = np.array(["Lombardy","Tuscany"])
    
    def __init__(self,service_name,service_type,address,gps_position):
        self.service_name = service_name
        self.address = address;
        self.service_type = service_type
        self.department = str(np.random.choice(self.DEPARTMENTS))
        self.gps_position = gps_position


class AuthBodyFactory:
    
    SERVICE_NAMES = np.array(["hospital","pharmacy"])
    
    
    def __init__(self,address_generator,csv_base_path):
        self.address_generator = address_generator
        hospitals_df = pd.read_csv(csv_base_path+"hospitals.csv",encoding = "ISO-8859-1")
        pharmacies_df = pd.read_csv(csv_base_path+"pharmacies.csv",encoding = "ISO-8859-1",sep=';')
        self.hospital_names = np.array(hospitals_df["name"].tolist())
        self.pharmacy_names = np.array(pharmacies_df["name"].tolist())
    
    def generate_auth_bodys(self,number_of_entities):
        hospitals_count = min(np.random.randint(1,number_of_entities),len(self.hospital_names))
        pharmacies_count = min(number_of_entities-hospitals_count,len(self.pharmacy_names))
        
        hospitals = np.random.choice(self.hospital_names,hospitals_count)
        pharmacies = np.random.choice(self.pharmacy_names,pharmacies_count)

        result = []
        for name in hospitals:
            address, gps_position = self.address_generator.generate_address_and_gps()
            result.append(AuthBody(str(name),"hospital",address,gps_position))
        for name in pharmacies:
            address, gps_position = self.address_generator.generate_address_and_gps()
            result.append(AuthBody(str(name),"pharmacy",address,gps_position))
        
        return result
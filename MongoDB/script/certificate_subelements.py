# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 16:22:00 2021

@author: matteo
"""

import numpy as np
import datetime
import generator_utils as ut

class VaccineLot:
    def __init__(self,brand,vaccine_type,lot,production_date):
        self.brand = brand
        self.vaccine_type = vaccine_type
        self.lot = lot
        self.production_date = production_date

class VaccineLotsGenerator:
    
    VACCINES_DEVELOPMENT_TIME = 300 #days to start vaccinations
    VACCINE_BRANDS=np.array(["Pfizer","Moderna","AstraZeneca"])
    
    #for simplicy, each brand make vaccines all of the same type (and I think that at the moment this is also true)
    VACCINE_TYPES = {
        "Pfizer":"mRna",
        "Moderna":"mRna",
        "AstraZeneca":"Viral Vector"
        }
    
    LOT_LENGTH = 7
    
    def __init__(self,pandemy_time_interval,number_of_lots):
        self.lots = []
        start_date = pandemy_time_interval[0] + datetime.timedelta(days=self.VACCINES_DEVELOPMENT_TIME)
        if start_date > pandemy_time_interval[1]: #if the pandemy interval is too small just use the begin of the pandemy for such a small example
            start_date = pandemy_time_interval[0]
        for i in range(number_of_lots):
            production_date = ut.random_date(start_date,pandemy_time_interval[1])
            brand = str(np.random.choice(self.VACCINE_BRANDS)) #I dont' know why, but in this case it returns a numpy version of string (but, for instance, with the names it returns a string)
            vaccine_type = self.VACCINE_TYPES[brand]
            lot = str(i).rjust(self.LOT_LENGTH,"L")
            self.lots.append(VaccineLot(brand,vaccine_type,lot,production_date))
        self.lots.sort(key=lambda l:l.production_date)
    
    def get_lot(self,max_production_date):
        i = 0
        while i<len(self.lots) and self.lots[i].production_date<=max_production_date:
            i = i + 1
        max_index = i-1
        return self.lots[np.random.randint(max_index)]
    
    def get_first_rpduction_date(self):
        return self.lots[0].production_date

class MedicalEmployee:
    
    def __init__(self,bedge_id,role,name):
        self.bedge_id = bedge_id
        self.role = role
        self.name = name

class MedicalEmployeesGenerator:
    
    BEDGE_ID_LENGTH = 7
    
    def __init__(self,number_of_doctors,number_of_nurses,names_generator):
        self.doctors = []
        self.nurses = []
        for i in range(number_of_doctors):
            bedge_id = str(i).rjust(self.BEDGE_ID_LENGTH,"B")
            name = names_generator.get_name()
            self.doctors.append(MedicalEmployee(bedge_id,"Doctor",name))
        for i in range(number_of_nurses):
            bedge_id = str(i).rjust(self.BEDGE_ID_LENGTH,"B")
            name = names_generator.get_name()
            self.nurses.append(MedicalEmployee(bedge_id,"Nurse",name))
        self.doctors = np.array(self.doctors)
        self.nurses = np.array(self.nurses)
        
    def get_doctor(self):
        return np.random.choice(self.doctors)

    def get_nurse(self):
        return np.random.choice(self.nurses)
    
    def get_couple(self):
        return (self.get_doctor(),self.get_nurse())
    
class Vaccination:
    
    def __init__(self,issuing_date,address,lot,employees,use_lot=False):
        self.issuing_date = issuing_date
        self.address = address
        #depend on how to generate the json
        if use_lot:
            self.lot = lot
        else:
            self.lot = lot.lot
            self.brand = lot.brand
            self.vaccine_type = lot.vaccine_type
            self.production_date = lot.production_date
        self.employees = employees


class Test:
    
    def __init__(self,issuing_date,positive,address,employees):
        self.issuing_date = issuing_date
        self.positive = positive
        self.address = address
        self.employees = employees
    
class EmergencyContact:
    
    def __init__(self,name,phone_number,email,address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address

class Person:
    
    def __init__(self,ssn,name,birth_date,address,height,weight):
        self.ssn = ssn
        self.name = name
        self.birth_date = birth_date
        self.address = address
        self.height = height
        self.weight = weight
    
    
    
    
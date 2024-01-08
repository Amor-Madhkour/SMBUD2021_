# -*- coding: utf-8 -*-

import numpy as np
import datetime
import generator_utils as ut
import pandas as pd

class Person:
    """
    A person with its vaccinations and both positive and negative tests.
    May be currently infected
    """
    
    VACCINE_NAMES=np.array(["Pfizer","Moderna","AstraZeneca"])
    VACCINE_PROB = 0.8
    VACCINE_FIRST_DATE = datetime.date(2020, 11, 1) #randomly start vaccines from here
    MAX_DAYS_BETTWEN_VACCINES = 15 #just for simplicty, all vaccines have the same interval
    
    MAX_RANDOM_NEGATIVE_TESTS = 4 #max test without being infected
    NO_RANDOM_TESTS_PROB = 0.2 #just to increase the probability of people without negative tests
    
    HAS_BEEN_INFECTED_PROB = 0.2 #a bit pessimistic, but we have a few nodes only
    CURRENTLY_INFECTED_PROB = 0.2
    RECOVERY_DAYS = 10
    HEALED_PROB = 0.7 #probability of being healed after RECOVERY_DAYS
    
    TWO_ADDRESSES_PROB = 0.2
    
    
    #pandemy_time_interval is the pandemic interval.. remember to include VACCINE_FIRST_DATE in it
    def __init__(self,code,name,address_generator,birth_range,pandemy_time_interval,devices):
        self.name = name
        self.birth_date = ut.random_date(min(birth_range[0],pandemy_time_interval[0]),min(birth_range[1],pandemy_time_interval[1]))
        self._generate_addresses(address_generator,pandemy_time_interval)
        self.code = code
        tests_place = address_generator.generate_address() #for the sake of simplicity let's assume that a person takes tests alwys in the same place
        self._generate_vaccines(address_generator,pandemy_time_interval[1])
        self._generate_negative_tests(pandemy_time_interval,tests_place)
        self._generate_old_infections(pandemy_time_interval,tests_place)
        if np.random.rand()<=self.CURRENTLY_INFECTED_PROB:
            test_date = ut.random_date(pandemy_time_interval[1]+datetime.timedelta(days=1), pandemy_time_interval[1]+datetime.timedelta(days=5))
            self.tests.append(Test(test_date,True,tests_place))
        self.devices = devices
    
    def _generate_addresses(self,address_generator,pandemy_time_interval):
        if(np.random.rand()<=self.TWO_ADDRESSES_PROB):
            self.addresses = [AddressPeriod(address_generator.generate_address(),self.birth_date,None)]
        else:
            change_date = ut.random_date(max(pandemy_time_interval[0],self.birth_date),pandemy_time_interval[1])
            self.addresses = [AddressPeriod(address_generator.generate_address(),self.birth_date,change_date),
                              AddressPeriod(address_generator.generate_address(),change_date,None)]
            #there is a small probability that the two addresses are the same one....
    
    def _generate_vaccines(self,address_generator,end_date):
        self.vaccinations = []
        if(np.random.rand()<=self.VACCINE_PROB):
            vaccine_name = np.random.choice(self.VACCINE_NAMES)
            first_date = ut.random_date(self.VACCINE_FIRST_DATE,end_date)
            address = address_generator.generate_address() #all vaccines at the same place
            self.vaccinations.append(Vaccination(first_date,address,vaccine_name))
            if (end_date-first_date).days>=self.MAX_DAYS_BETTWEN_VACCINES:
                random_noise = np.random.randint(-1,1) #the second vaccination is not exactly x times after the first
                second_date = first_date + datetime.timedelta(days=self.MAX_DAYS_BETTWEN_VACCINES+random_noise)
                self.vaccinations.append(Vaccination(second_date,address,vaccine_name))
    
    def _generate_negative_tests(self,time_interval,tests_place):
        self.tests=[]
        if np.random.rand()<=self.NO_RANDOM_TESTS_PROB :
            return
        test_count = np.random.randint(0,self.MAX_RANDOM_NEGATIVE_TESTS)
        for i in range(test_count):
            test_date = ut.random_date(time_interval[0], time_interval[1])
            self.tests.append(Test(test_date,False,tests_place))
    
    def _generate_old_infections(self,time_interval,tests_place):
        while(np.random.rand()<=self.HAS_BEEN_INFECTED_PROB): #he might have been infected multiple times
            infection_date = ut.random_date(time_interval[0], time_interval[1])
            self.tests.append(Test(infection_date,True,tests_place))
            test_date = infection_date + datetime.timedelta(days=self.RECOVERY_DAYS)
            while(test_date<time_interval[1]): #there is a small probability that he is still infected at the end of time_interval
                test_date = test_date + datetime.timedelta(days=self.RECOVERY_DAYS+np.random.randint(-2,+2)) #next test date
                if np.random.rand()<self.HEALED_PROB:  #healed
                    self.tests.append(Test(test_date,False,tests_place))
                    break;
                else:
                    self.tests.append(Test(test_date,True,tests_place)) #he made another test and was found infected again
                    

class AddressPeriod:
    def __init__(self,address,start_date,end_date):
        self.address = address
        self.start_date = start_date
        self.end_date = end_date

class Vaccination:
    
    def __init__(self,date,address,vaccine):
        self.date = date
        self.address = address
        self.vaccine = vaccine



class Test:
    
    def __init__(self,date,result,address):
        self.date = date
        self.result = result #true if positive, false otherwise
        self.address = address


class Device:
    
    def __init__(self, device_id, device_category):
        self.device_id = device_id
        self.category = device_category

class DeviceFactory:
    ID_LENGTH = 16
    def __init__(self):
        self.current_id = 0
    
    def generate_device(self,category):
        device = Device(str(self.current_id).rjust(self.ID_LENGTH,"D"),category)
        self.current_id = self.current_id + 1
        return device

class PersonFactory:
    
    BIRTH_RANGE = (datetime.date(1930,1,1),datetime.date.today())
    ID_LENGTH = 16
    TWO_DEVICES_PROB = 0.3
        
    def __init__(self,address_generator,pandemy_time_interval,csv_base_path):
        self.names = np.array(pd.read_csv(csv_base_path+"names.csv").iloc[:,0])
        self.address_generator = address_generator
        self.pandemy_time_interval = pandemy_time_interval
        self.current_id = 0
        self.deviceFactory = DeviceFactory()
        
    #for sake of simplicy, identifier are generated from sequential ids (but they are strings)
    #given a country, its identifier should be used (e.g. codice fiscale)
    def generate_person(self):
        identifier = str(self.current_id)
        identifier = identifier.rjust(self.ID_LENGTH,"X")
        self.current_id+=1
        name = np.random.choice(self.names)
        devices = [self.deviceFactory.generate_device("Smartphone")]
        if np.random.rand()<=self.TWO_DEVICES_PROB:
            devices.append(self.deviceFactory.generate_device("Smartwatch"))
            #for simplicity consider just two categories and at most 2 devices for person
        return Person(identifier,name,self.address_generator,self.BIRTH_RANGE,self.pandemy_time_interval,devices)






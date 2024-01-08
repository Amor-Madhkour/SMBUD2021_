# -*- coding: utf-8 -*-

import numpy as np
import datetime
import generator_utils as ut
import certificate_subelements as subel

class Certificate:
    
    
    VACCINATED_PROB = 0.8
    TESTED_PROB = 0.7
    
    DAYS_BETWEEN_VACCINATIONS = [(15,20),(180,200)] #at index i the range of days between the dose i and the dose i+1
    
    MAX_TESTS = 3 #max number of tests for certificate
    POSITIVE_TEST_PROB = 0.2 #probability for a test to be positive 
    
    
    
    #pandemy_time_interval is the pandemic interval.. remember to include VACCINE_FIRST_DATE in it
    def __init__(self,person,emergency_contact,pandemy_time_interval,vaccinations_start_date,
                 address_generator,lots_generator,employees_generator,
                 use_person=False,use_lot=False):
        #depending on how you want the json to be created
        if use_person:
            self.person = person
        else:
            self.ssn = person.ssn
            self.name = person.name
            self.birth_date = person.birth_date
            self.address = person.address
            self.weight = person.weight
            self.height = person.height
            
        vaccinated = np.random.rand()<=self.VACCINATED_PROB
        self.vaccinations = []
        self.tests = []
        if vaccinated:        
            self._generate_vaccinations(address_generator, lots_generator, employees_generator,
                                        vaccinations_start_date, pandemy_time_interval[1],use_lot)
        if np.random.rand()<=self.TESTED_PROB or not vaccinated: #do not to generate a certificate with neither vaccinations nor tests
            self._generate_tests(address_generator, employees_generator, pandemy_time_interval)

        self.emergency_contact = emergency_contact
        
    def _generate_vaccinations(self,address_generator,lots_generator,employees_generator,start_date,end_date,use_lot):
        self.vaccinations = []
        number_of_doses = np.random.randint(1,3);
        issuing_date = ut.random_date(start_date,end_date)
        for i in range(number_of_doses):
            lot = lots_generator.get_lot(end_date)
            address = address_generator.generate_address()
            employees = list(employees_generator.get_couple())
            self.vaccinations.append(subel.Vaccination(issuing_date, address, lot, employees,use_lot))
            #now prepare the next issuing_date
            new_dose_delay = np.random.randint(self.DAYS_BETWEEN_VACCINATIONS[i][0],self.DAYS_BETWEEN_VACCINATIONS[i][1])
            issuing_date = issuing_date + datetime.timedelta(days=new_dose_delay)
            if issuing_date>end_date: #if the more or less random dates bring me out of the pandemic interval, do not add a new dose
                break
    
    #these are really random
    def _generate_tests(self,address_generator,employees_generator,pandemy_time_interval):
        self.tests = []
        test_count = np.random.randint(1,self.MAX_TESTS)
        used_dates = set() #just not to repat dates
        for i in range(test_count):
            issuing_date = ut.random_date(pandemy_time_interval[0], pandemy_time_interval[1])
            if issuing_date in used_dates:
                continue
            used_dates.add(issuing_date)
            positive = True if np.random.rand()<=self.POSITIVE_TEST_PROB else False
            address = address_generator.generate_address()
            employees = [employees_generator.get_doctor()]
            if np.random.random()<=0.3: #sometimes add a nurse
                employees.append(employees_generator.get_nurse())
            self.tests.append(subel.Test(issuing_date, positive, address, employees))
        self.tests.sort(key=lambda x:x.issuing_date)
    
class CertificateFactory:
    
    BIRTH_RANGE = (datetime.date(1930,1,1),datetime.date.today())
    TWO_DEVICES_PROB = 0.3
    VACCINATION_START_DELAY = 3 # days from the production of the first lot to the begin of the vaccinations
    
    SSN_LENGTH = 10
    HEIGHT_RANGE = (1.4,2.0)
    WEIGHT_RANGE = (50,90)
    
    def __init__(self,pandemy_time_interval,
                  address_generator,names_generator,lots_generator,employees_generator):
        self.address_generator = address_generator
        self.names_generator = names_generator
        self.lots_generator = lots_generator
        self.employees_generator = employees_generator
        self.pandemy_time_interval = pandemy_time_interval
        self.current_id = 0
        self.vaccinations_start_date = lots_generator.get_first_rpduction_date() + datetime.timedelta(days=self.VACCINATION_START_DELAY)
        
    #for sake of simplicy, identifier are generated from sequential ids (but they are strings)
    #given a country, its identifier should be used (e.g. codice fiscale)
    def generate_certificate(self,use_person=False,use_lot=False):
        ssn = str(self.current_id).rjust(self.SSN_LENGTH,"X")
        self.current_id+=1
        name = self.names_generator.get_name()
        ssn = ssn
        name = name
        birth_date = ut.random_date(min(self.BIRTH_RANGE[0],self.pandemy_time_interval[0]),
                                    min(self.BIRTH_RANGE[1],self.pandemy_time_interval[0]))
        #for simplicity do not consider people born during the pandemy, so that there isn't the possibility that they result vaccinated before being born
        address = self.address_generator.generate_address()
        height = round(np.random.uniform(self.HEIGHT_RANGE[0],self.HEIGHT_RANGE[1]), 1) #float
        weight = np.random.randint(self.WEIGHT_RANGE[0],self.WEIGHT_RANGE[1]) #int
        person = subel.Person(ssn, name, birth_date,address,height,weight)
        emergency_contact = subel.EmergencyContact(self.names_generator.get_name(),
                                                   "12345000"+str(self.current_id),
                                                   "person"+str(self.current_id)+"@something.com",
                                                   self.address_generator.generate_address())
        return Certificate(person, emergency_contact, self.pandemy_time_interval,
                           self.vaccinations_start_date, self.address_generator, self.lots_generator, self.employees_generator,
                           use_person,use_lot)






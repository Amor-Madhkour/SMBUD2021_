# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime
import networkx as nx


class AddressGenerator:
    MAX_ADDRESS_NUMBER = 30
    
    def __init__(self,csv_base_path):
        self.city_names = np.array(pd.read_csv(csv_base_path+"cities.csv",encoding = "ISO-8859-1").iloc[:,0])
        self.street_names = np.array(pd.read_csv(csv_base_path+"streets.csv",encoding = "ISO-8859-1").iloc[:,0])
        self.addresses = set()
    
    def generate_address(self):
        city = self.city_names[np.random.randint(0,len(self.city_names))]
        street = self.street_names[np.random.randint(0,len(self.street_names))]
        number = np.random.randint(1,self.MAX_ADDRESS_NUMBER+1)
        address = Address(street+" "+str(number),city)
        self.addresses.add(address)
        return address

class Address:
    def __init__(self,addr,city):
        self.addr = addr
        self.city = city
        
    def __eq__(self, o):
        return self.addr == o.addr and self.city == o.city
    
    def __hash__(self):
        return hash ((self.addr,self.city))


#takes two dates and return a date, no datetime
#if you pass datetimes, it returns a datetime, but doesn't consider hours and minutes
def random_date(start_date,end_date):
    days_between_dates = (end_date-start_date).days
    if(days_between_dates == 0):
        delta = 0
    else:        
        delta = np.random.randint(0,days_between_dates)
    return start_date + datetime.timedelta(days=delta)

#start and date are datetime
def random_datetime(start,end):
    seconds_between_dates = (end-start).total_seconds()
    if(seconds_between_dates == 0):
        delta = 0
    else:        
        delta = np.random.randint(0,seconds_between_dates)
    return start + datetime.timedelta(seconds=delta)

def random_datetime_interval(start,end,max_duration_seconds=None):
    time1 = random_datetime(start,end)
    if not max_duration_seconds == None:
        temp = time1+datetime.timedelta(seconds=max_duration_seconds)
        if temp<end:
            end = temp
    time2 = random_datetime(time1,end)
    return (time1.replace(minute=0,second=0,microsecond=0), #we consider only up to hours
                time2.replace(minute=0,second=0,microsecond=0))

def date_to_datetime(date):
    return datetime.datetime(date.year,date.month,date.day)

#can be used to returns the date in a format that neo4j can manage
#notice that neo4j has different functions to generate dates from strings, so we can sue them too
def date_to_neo4j(date):
    return str(date)

def datetime_to_neo4j(date):
    return str(date)

def generate_contacts(people,time_interval,max_single_person_contacts):
    n = len(people)
    p = 1/n
    contacts_graph = nx.erdos_renyi_graph(n,p,directed=False)
    contacts = []
    for edge in contacts_graph.edges:
        contacts_count = np.random.randint(1,max_single_person_contacts)
        for i in range(contacts_count): #generate multiple contacts with the same pair of people
            date = random_date(time_interval[0],time_interval[1])
            date = date_to_datetime(date)
            hours = np.random.randint(1,24)
            minutes = np.random.randint(1,60)
            date = date+datetime.timedelta(hours=hours,minutes=minutes)
            contacts.append( Contact(people[edge[0]],people[edge[1]],date) )
    return contacts

class Contact:
    
    def __init__(self,person1,person2,time):
        self.person1 = person1
        self.person2 = person2
        self.time = time
    

#generate groups of peoples as array of array    
def generate_groups(people,max_group_members):
    np.random.shuffle(people)
    i=0
    result =[]
    while i<len(people):
        group_count = min(len(people)-i,np.random.randint(1,max_group_members))
        if group_count == 1:
            i = i+1
            continue;
        result.append(people[i:i+group_count])
        i = i + group_count
    return result
    

MAX_FAMILY = 5
MAX_WORK = 20
FREQ_PROB = 0.1 #probability a Frequent_contact ends or starts during the pandemy
START_RELATION_DATE = datetime.date(year=1950,month=1,day=1)

def generate_frequent_contacts(people,pandemy_time_interval):
    families = generate_groups(people,MAX_FAMILY)
    work_groups = generate_groups(people,min(MAX_WORK,len(people)/3))
    groups = families + work_groups
    result = []
    #now create relations
    #most relations start before the pandemy and haven't end yet
    for group in groups:
        for i in range(len(group)-1):
            start_date = random_date(START_RELATION_DATE,pandemy_time_interval[0])
            end_date = None
            if np.random.rand()<=FREQ_PROB:
                if np.random.rand()<0.5:
                    end_date = random_date(pandemy_time_interval[0],pandemy_time_interval[1])
                else:
                    start_date = random_date(pandemy_time_interval[0],pandemy_time_interval[1])
            for j in range(i+1,len(group)):
                result.append(Frequent_contact(group[i],group[j],start_date,end_date))
    
    #this is not efficient, but it works and avoid strange things
    #note: cypher MERGE alone isn't enough to avoid strange things,
    #so I jus tmake sure that there is a single frequent contact for each couple to avoid unexpected cases
    result_always_different_couples = []
    for i in range(len(result)-1):
        flag = True
        for j in range(i+1,len(result)-1):
            if (result[j].person1.code == result[i].person1.code and result[j].person2.code == result[i].person2.code) or (result[j].person1.code == result[i].person2.code and result[j].person2.code == result[i].person1.code):
                flag = False
                break;
        if flag:
            result_always_different_couples.append(result[i])
    return result_always_different_couples


class Frequent_contact:
    def __init__(self,p1,p2,start_date,end_date):
        self.person1 = p1
        self.person2 = p2
        self.start_date = start_date
        self.end_date = end_date #may be None






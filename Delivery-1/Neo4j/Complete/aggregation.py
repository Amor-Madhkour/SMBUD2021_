# -*- coding: utf-8 -*-

import generator_utils as ut
import datetime
import numpy as np

class Aggregation:
    
    
    #time_interval is a tuple of datetime.date, hours are added randomly
    def __init__(self,name,start,end,participations,address):
        self.name = name
        self.participations = participations
        self.address = address #may be none
        self.start_time = start
        self.end_time = end


class Participation:
    def __init__(self,person,start_time,end_time):
        self.person = person
        self.start_time = start_time
        self.end_time = end_time

class AggregationFactory:
    MAX_SHORT_AGGREGATION_SECONDS = 5*3600
    SHORT_NAMES = np.array(["Concert ", "Match "])
    NO_ADDRESS_NAMES = np.array(["Flight Number "])

    LONG_NAMES = np.array(["Museum visit "]) #activities that started before the pandemy and aren't finished yet
    MAX_PARTICIPATIONS_IN_LONG = 2
    
    SHORT_COUNT_RANGE = (1,5)
    LONG_COUNT_RANGE = (1,5)
    NO_ADDRESS_COUNT_RANGE = (1,3)
    
    LONG_START = datetime.datetime(2010, 1, 1) #start date for places that have been open since before the pandemy
    
    def __init__(self,pandemy_time_interval,people,address_generator):
        self.current_id = 0
        self.pandemy_time_interval = (ut.date_to_datetime(pandemy_time_interval[0]), 
                                      ut.date_to_datetime(pandemy_time_interval[1]))
        self.people = people
        self.max_participants = min(30,len(people))
        self.max_low_participants = min(10,len(people))
        self.address_generator= address_generator
    
    def generate_short_aggregation(self):
        max_part = self.max_participants if np.random.rand()<=0.5 else self.max_low_participants #50% have the possibility to be a big event, else it's a small one
        participants = np.random.choice(self.people,size=np.random.randint(2,max_part))
        start, end = self._generate_short_duration()
        participations = [Participation(p, start, end) for p in participants] #for simplicity they all stay for the full event
        name = self._generate_name(self.SHORT_NAMES)
        return Aggregation(name,start,end,participations,self.address_generator.generate_address())
    
    def generate_no_address_aggreagation(self):
        participants = np.random.choice(self.people,size=np.random.randint(2,self.max_participants))
        start, end = self._generate_short_duration()
        participations = [Participation(p, start, end) for p in participants] #in a train that does multiple stops they may have different participations time, but in this case I consider only flights
        name = self._generate_name(self.NO_ADDRESS_NAMES)
        return Aggregation(name,start,end,participations,None)
    
    def generate_long_aggregation(self,): #people may even participate multiple times to the same long aggregation (visit a museum 2 times?)
        participants = np.random.choice(self.people,size=np.random.randint(2,len(self.people)/3))
        participations = []
        start, end = self._generate_long_duration()
        for p in participants:
            #choose number of times using randint(1,MAX_PARTICIPATIONS_IN_LONG), check that it includes the extreme
            count = np.random.randint(1,self.MAX_PARTICIPATIONS_IN_LONG)
            p_end = start #avoid overlapping: next one starts after the previous one
            for i in range(count): #there is a very small probability of an overlapping
                p_start, p_end = self._generate_partecipation_time(p_end,self.pandemy_time_interval[1]) #from last visit to the ned of the pandemy
                participations.append(Participation(p, p_start, p_end))
        name = self._generate_name(self.LONG_NAMES)
        return Aggregation(name,start,end,participations,self.address_generator.generate_address())
    
    def generate_all_aggregations(self):
        aggregations = []
        aggregations_count = np.random.randint(self.SHORT_COUNT_RANGE[0],self.SHORT_COUNT_RANGE[1])
        for i in range(aggregations_count):
            aggregations.append(self.generate_short_aggregation())
        aggregations_count = np.random.randint(self.NO_ADDRESS_COUNT_RANGE[0],self.NO_ADDRESS_COUNT_RANGE[1])
        for i in range(aggregations_count):
            aggregations.append(self.generate_no_address_aggreagation())
        aggregations_count = np.random.randint(self.LONG_COUNT_RANGE[0],self.LONG_COUNT_RANGE[1])
        for i in range(aggregations_count):
            aggregations.append(self.generate_long_aggregation())
        return aggregations
    
    #for simplicty consider only hours, no minutes or seconds
    def _generate_short_duration(self):
        return ut.random_datetime_interval(self.pandemy_time_interval[0],self.pandemy_time_interval[1],
                                               self.MAX_SHORT_AGGREGATION_SECONDS)
    
    def _generate_partecipation_time(self,start,end):
        return ut.random_datetime_interval(start,end)
    
    def _generate_long_duration(self):
        return ut.date_to_datetime(ut.random_date(self.LONG_START,self.pandemy_time_interval[0])), None # it starts before the pandemy and has not ended
    
    
    def _generate_name(self,possibilities):
        name = np.random.choice(possibilities) + str(self.current_id) #for simplicty, generate unique names
        self.current_id = self.current_id+1
        return name


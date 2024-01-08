# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime


class AddressGenerator:
    MAX_ADDRESS_NUMBER = 30
    CITIES_TO_USE = 10
    MAX_DISTANCE_FROM_CENTER = 0.005
    
    def __init__(self,csv_base_path):
        cities_df = pd.read_csv(csv_base_path+"cities_and_gps.csv",encoding = "utf-8")
        cities_df=cities_df.sample(frac=1)
        self.city_names = cities_df["name"].tolist()
        self.city_names = self.city_names[:min(self.CITIES_TO_USE,len(self.city_names))]
        self.latitudes = cities_df["latitude"].tolist()
        self.latitudes = self.latitudes[:min(self.CITIES_TO_USE,len(self.latitudes))]
        self.longitudes = cities_df["longitude"].tolist()
        self.longitudes = self.longitudes[:min(self.CITIES_TO_USE,len(self.longitudes))]
        self.street_names = np.array(pd.read_csv(csv_base_path+"streets.csv",encoding = "ISO-8859-1").iloc[:,0])
        
    
    def generate_address(self):
        return self.generate_address_and_gps()[0]
    
    def generate_address_and_gps(self):
        """
        Generate an adddress and it's gps position (address,gps position)
        Notice that if the same address is generated again, a new gps location is generated
        """
        #print(self.city_names)
        city_index = np.random.randint(0,len(self.city_names))
        city = self.city_names[city_index]
        street = self.street_names[np.random.randint(0,len(self.street_names))]
        number = np.random.randint(1,self.MAX_ADDRESS_NUMBER+1)
        address = city+", "+street+" "+str(number)
        latitude = float(self.latitudes[city_index]) + np.random.rand()*self.MAX_DISTANCE_FROM_CENTER
        longitude = float(self.longitudes[city_index]) + np.random.rand()*self.MAX_DISTANCE_FROM_CENTER
        return address, GPSPosition(longitude=longitude,latitude=latitude)



class NamesGenerator:
        
    def __init__(self,csv_base_path):
        self.names = np.array(pd.read_csv(csv_base_path+"names.csv").iloc[:,0])
    
    def get_name(self):
        return np.random.choice(self.names)

class GPSPosition:
    
    def __init__(self,longitude,latitude):
        self.latitude = latitude
        self.longitude = longitude

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

#can be used to returns the date in a format that the database can easily import
def date_to_db(date):
    #return "ISODate('"+str(date)+"T00:00:00.000Z"+"')" #doesn't work... evn if you manually make it not a string
    return str(date)+"T00:00:00.000Z"

def datetime_to_db(date):
    return str(date)+"T00:00:00.000Z"
    ##for mongodb I have no datetime...




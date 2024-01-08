# -*- coding: utf-8 -*-

import numpy as np
import datetime
import csv

import generator_utils as ut
import person as person_mod
import aggregation as aggregation_mod

#I use np.random and not the python random since some array-wise random funcitons may be useful

PANDEMY_TIME_INTERVAL = (datetime.date(2021,5,1),datetime.date(2021,7,1)) #compress the range in order no to have tests and contacts too sparse

PEOPLE_COUNT_RANGE = (40,60)

MAX_SINGLE_PERSON_CONTACTS = 3

CSV_BASE_PATH = "csv/"

ad_gen = ut.AddressGenerator(CSV_BASE_PATH)
p_factory = person_mod.PersonFactory(ad_gen,PANDEMY_TIME_INTERVAL,CSV_BASE_PATH)


people_count  = np.random.randint(PEOPLE_COUNT_RANGE[0],PEOPLE_COUNT_RANGE[1])
people = []
for i in range(people_count):
    people.append(p_factory.generate_person())
people = np.array(people)

contacts = ut.generate_contacts(people, PANDEMY_TIME_INTERVAL, MAX_SINGLE_PERSON_CONTACTS)

a_factory = aggregation_mod.AggregationFactory(PANDEMY_TIME_INTERVAL, people,ad_gen)
aggregations = a_factory.generate_all_aggregations()


frequent_contacts = ut.generate_frequent_contacts(people,PANDEMY_TIME_INTERVAL)


encoding = "utf-8"

with open(CSV_BASE_PATH+"people.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["code","name","birth_date"])
    for p in people:
        row = [p.code, p.name, ut.date_to_neo4j(p.birth_date)]
        csv_writer.writerow(row)

with open(CSV_BASE_PATH+"person_addresses.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["person","address","city","start_date","end_date"])
    for p in people:
        for addressPeriod in p.addresses:
            end_date = "null" if addressPeriod.end_date is None else ut.datetime_to_neo4j(addressPeriod.end_date)
            start_date = ut.date_to_neo4j(addressPeriod.start_date)
            row = [p.code, addressPeriod.address.addr, addressPeriod.address.city, start_date, end_date]
            csv_writer.writerow(row)

with open(CSV_BASE_PATH+"devices.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["device_id","device_category","person"])
    for p in people:
        for d in p.devices:
            row = [d.device_id, d.category, p.code]
            csv_writer.writerow(row)

with open(CSV_BASE_PATH+"tests.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["person","date","positive","address","city"])
    for p in people:
        for test in p.tests:            
            row = [p.code, ut.date_to_neo4j(test.date), test.result, test.address.addr, test.address.city]
            csv_writer.writerow(row)

with open(CSV_BASE_PATH+"vaccinations.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["person","date","vaccine","address","city"])
    for p in people:
        for vaccination in p.vaccinations:            
            row = [p.code, ut.date_to_neo4j(vaccination.date), vaccination.vaccine,
                   vaccination.address.addr, vaccination.address.city]
            csv_writer.writerow(row)

with open(CSV_BASE_PATH+"contacts.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["person1","person2","time"])
    for c in contacts:
        row = [c.person1.code, c.person2.code, ut.datetime_to_neo4j(c.time)]
        csv_writer.writerow(row)

with open(CSV_BASE_PATH+"aggregations.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["name","start_time","end_time","address","city"])
    for aggregation in aggregations:
        if aggregation.address is None:
            addr = "null"
            city = "null"
        else:
            addr = aggregation.address.addr
            city = aggregation.address.city
        if aggregation.end_time is None:
            end_time = "null"
        else:
            end_time = ut.datetime_to_neo4j(aggregation.end_time)
        row = [aggregation.name,
               ut.datetime_to_neo4j(aggregation.start_time), end_time,
               addr, city]
        csv_writer.writerow(row)

with open(CSV_BASE_PATH+"participations.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["aggregation_name","aggregation_start","person","start_time","end_time"])
    for aggregation in aggregations:
        #print("Event {} has {} participants".format(event.id,len(event.participations)))
        for p in aggregation.participations:
            row = [aggregation.name, ut.datetime_to_neo4j(aggregation.start_time),
                   p.person.code, ut.datetime_to_neo4j(p.start_time), ut.datetime_to_neo4j(p.end_time)]
            csv_writer.writerow(row)

with open(CSV_BASE_PATH+"addresses.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["addr","city"])
    for address in ad_gen.addresses:
        row = [address.addr,address.city]
        csv_writer.writerow(row)

with open(CSV_BASE_PATH+"frequent_contacts.csv",mode = "w",newline='',encoding = encoding) as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["person1","person2","start_date","end_date"])
    for c in frequent_contacts:
        if c.end_date is None:
            end_date = "null"
        else:
            end_date = ut.date_to_neo4j(c.end_date)
        row = [c.person1.code, c.person2.code, ut.date_to_neo4j(c.start_date),end_date]
        csv_writer.writerow(row)
    

    
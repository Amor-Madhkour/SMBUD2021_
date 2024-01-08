# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 14:07:05 2021

@author: matteo
"""

import pandas as pd
import numpy as np
import random
import csv
import networkx as nx
import matplotlib.pyplot as plt

#for the sake of simplicity, I use integers as times, not dates
MIN_TIME = 0
MAX_TIME = 10

MIN_EVENTS = 1
MAX_EVENTS = 20

MIN_PEOPLE = 2
MAX_PEOPLE = 5


data = pd.read_csv("test_people.csv")
names = data.iloc[:,0]
events = []
contacts = []
partecepiations = []
n = len(names)

p = 1/n
print("n:{},p:{}".format(n,p))
contacts_graph = nx.erdos_renyi_graph(n,p,directed=False)
nx.draw(contacts_graph) #to plot the graph... you may decide to remove this
plt.show() #to plot

for edge in contacts_graph.edges:
    time = random.randint(MIN_TIME, MAX_TIME)
    contacts.append( (names[edge[0]],names[edge[1]],time) )
    #if you want multiple contacts with the same people at different times,
    #or maybe creating multiple graphs and repeating this procedure multiple times:
    #the possibility of two contacts with the same people at the same time is so small that we can ignore it

events_count = random.randint(MIN_EVENTS,MAX_EVENTS)
for i in range(events_count):
    people = data.sample(n=random.randint(MIN_PEOPLE, MAX_PEOPLE)).iloc[:,0]
    time = random.randint(MIN_TIME, MAX_TIME)
    events.append( (i,time) ) #(["",""..],t)
    partecepiations.append(people)

with open("test_contacts.csv",mode = "w",newline='') as c_file:
    csv_writer = csv.writer(c_file,delimiter=",")
    csv_writer.writerow(["person1","person2","time"])
    csv_writer.writerows(contacts)
    

with open("test_events.csv",mode = "w",newline='') as e_file:
    csv_writer = csv.writer(e_file,delimiter=",")
    csv_writer.writerow(["event_id","time"])
    csv_writer.writerows(events)

with open("test_event_part.csv",mode = "w",newline='') as ep_file:
    csv_writer = csv.writer(ep_file,delimiter=",")
    csv_writer.writerow(["event_id","person"])
    for i in range(len(partecepiations)):
        for name in partecepiations[i]:
            csv_writer.writerow([i,name])



    
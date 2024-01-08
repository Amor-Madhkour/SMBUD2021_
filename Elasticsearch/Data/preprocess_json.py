# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:14:02 2022

@author: matteo
"""

import csv
import jsonpickle

class AgeGroup:
    
    def __init__(self,start,end):
        self.start = start
        if end is not None:
            self.end = end

class Record:
    
    def __init__(self,administration_date, supplier, area, age_start, age_end, male_count, female_count, 
          first_doses, second_doses, post_infection_doses, booster_doses, NUTS1_code, NUTS2_code,
          region_ISTAT_code, region_name):
        self.administration_date = administration_date
        self.supplier = supplier
        self.area = area
        self.age_group = AgeGroup(age_start,age_end)
        self.male_count = male_count
        self.female_count = female_count
        self.first_doses = first_doses
        self.second_doses = second_doses
        self.post_infection_doses = post_infection_doses
        self.booster_doses = booster_doses
        self.NUTS1_code = NUTS1_code
        self.NUTS2_code = NUTS2_code
        self.region_ISTAT_code = region_ISTAT_code
        self.region_name = region_name
        

age_index = 3
json_list = []
with open("somministrazioni-vaccini-latest.csv", 'r') as input_file:
    reader = csv.reader(input_file, delimiter=',')
    row1 = next(reader)
    for row in reader:
        #now split age_start-age_end. Remember that there is the esceptional case of 90+
        splitted_string = row[age_index].split("-")
        if(len(splitted_string)==2):
            age_start, age_end = splitted_string[0],splitted_string[1]
        else:
            age_start, age_end = 90, None
        record = Record(row[0],row[1],row[2],age_start,age_end,row[4],row[5],row[6],row[7],row[8],row[9],
                        row[10],row[11],row[12],row[13])
        json_list.append(record)

jsonpickle.set_encoder_options('json', indent=4)
with open("somministrazioni.json", 'w',newline='') as output_file:
    output_file.writelines("[\n")
    for i in range(len(json_list)-1):
        output_file.write(jsonpickle.encode(json_list[i], unpicklable=False))
        output_file.write(",\n")
    output_file.write(jsonpickle.encode(json_list[-1], unpicklable=False))    
    output_file.writelines("\n]\n")


# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:14:02 2022

@author: matteo
"""

import csv

istat_index = 12
#header = ["administration_date", "supplier", "area", "age_goup", "male_count", "female_count", 
#          "first_doses", "second_doses", "post_infection_doses", "booster_doses", "NUTS1_code", "NUTS2_code",
#          "region_ISTAT_code", "region_name"]
with open("somministrazioni-vaccini-latest.csv", 'r') as input_file, open("somministrazioni.csv", 'w',newline='') as output_file:
    reader = csv.reader(input_file, delimiter=',')
    writer = csv.writer(output_file)
    row1 = next(reader)
    header = row1
    print(header)
    writer.writerow(header)  
    for row in reader:
        istat_code = row[istat_index].rjust(2,'0')
        out_row = row[:istat_index]+[istat_code]+row[istat_index+1:]
        if not len(out_row)==len(row):
            print("error")
            break
        writer.writerow(out_row)
        

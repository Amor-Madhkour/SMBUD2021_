# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 15:51:02 2022

@author: matte
"""

import csv

header = ["area","NUTS1_code", "NUTS2_code","region_ISTAT_code", "region_name"]
area_index = 2
other_index = 10
with open("somministrazioni-vaccini-latest.csv", 'r') as input_file, open("regions.csv", 'w',newline='') as output_file:
    regions = set()
    reader = csv.reader(input_file, delimiter=',')
    writer = csv.writer(output_file)
    row1 = next(reader)
    print(header)
    writer.writerow(header)
    for row in reader:
        region = row[area_index]
        if region in regions:
            continue
        regions.add(region)        
        out_row = [region]+row[other_index:]
        writer.writerow(out_row)
        if (len(regions)==20):
            break
print("RMEMEBR TO PAD THE ISTAT CODE MANUALLY TO 2 DIGITS!!!")

#N.B. you still have to pad the istat_code manually!

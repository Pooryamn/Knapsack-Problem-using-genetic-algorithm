import csv  
import random
import numpy as np

def Read_Data():
    with open('Data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            Data.append(row)

    return Data

def Casting_Data(Data):
    # Casting data
    for i in range(1,len(Data)):
        for j in range(3):
            Data[i][j] = int(Data[i][j])

# main

Data = []
Population_Size = 20
Max_iteration = 1000
Max_weight = 165

Read_Data()
Casting_Data(Data)

print(Data)
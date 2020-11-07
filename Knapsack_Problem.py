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

def Fitness(Sample):
    return 0


def initialization(Data,Population_Size,Max_weight):
    

    choice_list = []
    Population_list = []
    for i in range(len(Data[:])):
        choice_list.append(i+1)

    i = 0
    while (i < Population_Size):
        subset_size = random.randint(1,len(Data[:]))
        sample = random.sample(choice_list,subset_size)
        
        if (Fitness(sample) > 0):
            Population_list.append(sample)
            i+=1


    return Population_list

# main

Data = []
Population_Size = 20
Max_iteration = 1000
Max_weight = 165

Read_Data()
Casting_Data(Data)

population = initialization(Data,Population_Size,Max_weight)
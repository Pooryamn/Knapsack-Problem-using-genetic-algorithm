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
    for i in range(len(Data)):
        for j in range(3):
            Data[i][j] = int(Data[i][j])


def Fitness(Sample,Max_weight,Data):

    # avoid repeating one stock twice or more
    if(Check_Duplicate_item(Sample) == True):
        return 0

    sample_weight = 0
    Sample_profit = 0

    # calculating sample weight
    for i in Sample:
        sample_weight += Data[i-1][1]
    
    if (sample_weight > Max_weight):
        # its not possible 
        return 0
    else:
        # it is a feasible answer
        # calculating sample profit
        for i in Sample:
            Sample_profit += Data[i-1][2]

        return Sample_profit 
    


def Check_Duplicate_item(Sample):
    if len(Sample) == len(set(Sample)):
        return False
    return True

def initialization(Data,Population_Size,Max_weight):
    

    choice_list = []
    Population_list = []
    for i in range(len(Data[:])):
        choice_list.append(i+1)

    i = 0
    while (i < Population_Size):
        subset_size = random.randint(1,len(Data[:]))
        sample = random.sample(choice_list,subset_size)
        
        if (Fitness(sample,Max_weight,Data) > 0):
            Population_list.append(sample)
            i+=1


    return Population_list

# main

Data = []
Population_Size = 200
Max_iteration = 1000
Max_weight = 165

Read_Data()
Casting_Data(Data)

population = initialization(Data,Population_Size,Max_weight)
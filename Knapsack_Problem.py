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
        sample_weight += Data[i][1]
    
    if (sample_weight > Max_weight):
        # its not possible 
        return 0
    else:
        # it is a feasible answer
        # calculating sample profit
        for i in Sample:
            Sample_profit += Data[i][2]

        return Sample_profit 
    


def Check_Duplicate_item(Sample):
    if len(Sample) == len(set(Sample)):
        return False
    return True

def initialization(Data,Population_Size,Max_weight):
    

    choice_list = []
    Population_list = []
    for i in range(len(Data[:])):
        choice_list.append(i)

    i = 0
    while (i < Population_Size):
        subset_size = random.randint(1,len(Data[:]))
        sample = random.sample(choice_list,subset_size)
        
        if (Fitness(sample,Max_weight,Data) > 0):
            Population_list.append(sample)
            i+=1


    return Population_list

def Knapsack(Max_iteration,Max_weight,population,Data):
    
    Data_size = len(Data)

    # iterations
    for iter in range(Max_iteration):
        
        # Cross over
        # in every iteration, cross over will done 200 times
        Children = []
        for i in range(400): 
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            parent1 = parent1[0:int(len(parent1)/2)+1]
            parent2 = parent2[int(len(parent2)/2):]
            Children.append(parent1 + parent2)

        # mutation
        for child in Children:
            mutation_thershold = random.randint(0,int((Data_size - len(child))/2))
            for j in range(mutation_thershold):
                child.append(random.choice(range(Data_size)))
        
        
        
        # calculate fitness and remove some unsuitable population
        feasible_population = []
        fit_arr = []
        for child in Children:
            # removing or calculating:
            tmp = Fitness(child,Max_weight,Data)
            if (Fitness(child,Max_weight,Data)> 0):
                feasible_population.append(child)
                fit_arr.append(tmp)
        
        
        # create population for the nex generation
        # roulette wheel
        sum_of_fitnesses = sum(fit_arr)

        # calculating probability array:
        P_array = []
        for personal_fitness in fit_arr:
            P_array.append(personal_fitness/sum_of_fitnesses) 
        
        # selecting randem children population using thier probability
        Children_no = int(0.75 * len(fit_arr))
        parent_no = int(0.25 * len(population))
        
        selected_child = random.choices(feasible_population,weights=P_array,k=Children_no)
        selected_parent = random.choices(population,k=Children_no)

        population = []
        population = selected_child + selected_parent

        # shffling the population
        random.shuffle(population)

    # final population:
    fit_arr = []
    for person in population:
            # removing or calculating:
            tmp = Fitness(person,Max_weight,Data)
            fit_arr.append(tmp)

    max_index = fit_arr.index(max(fit_arr))
    return population[max_index],fit_arr[max_index]

def Read_config():
    
    try:
        # try to open and read data
        Fp = open('Config.txt','r')
        All_lines = Fp.readlines()
        Fp.close()

        Variables  = []
        for line in All_lines:
            Variables.append(int(line.split()[2]))
        
        Max_iteration = Variables[0]
        Population_Size = Variables[1]
        Max_weight = Variables[2]

    except:
        # file doesn't exist
        print('File doesn\'t exist you should enter data manualy !')
        Max_iteration = int(input('Max iteration : '))
        Population_Size = int(input('Popultion size : '))
        Max_weight = int(input('Max_weight : '))

        Fp2 = open('Config.txt','w')
        Fp2.write('Max_iteration = {}\n'.format(Max_iteration))
        Fp2.write('Population_size = {}\n'.format(Population_Size))
        Fp2.write('Max_weight = {}\n'.format(Max_weight))
        Fp2.close()

    return Max_iteration,Population_Size,Max_weight

# main

Data = []

Max_iteration,Population_Size,Max_weight= Read_config()


Read_Data()
Casting_Data(Data)

# algorithm
population = initialization(Data,Population_Size,Max_weight)
person,profit = Knapsack(Max_iteration,Max_weight,population,Data)

solution_array = []
for i in range(len(Data)):
    solution_array.append(0)
for item in person:
    solution_array[item] = 1

print('Solution : {}'.format(solution_array))
print('Profit : {}'.format(profit))



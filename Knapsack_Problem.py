import csv  
import random
import numpy as np
from datetime import datetime
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Knapsack")
        self.setGeometry(50,50,350,350)
        self.setFixedWidth(960)
        self.setFixedHeight(540)
        self.UI()
        

    def UI(self):
        ########## Labels #########
            ## Back Ground image
        lbl_BG = QLabel("",self)
        lbl_BG.setGeometry(0,0,960,540)
        lbl_BG.setStyleSheet("border-image: url(img/BG.png);")
            ## weight label 
        lbl_weight = QLabel("     Max Weight : ",self)
        lbl_weight.setGeometry(80,20,200,30)
        lbl_weight.setFont(QFont('Times', 12))
            ## Population size label
        lbl_population = QLabel("Population Size : ",self)
        lbl_population.setGeometry(80,50,200,30)
        lbl_population.setFont(QFont('Times', 12))
            ## generation label
        lbl_weight = QLabel("      Generation : ",self)
        lbl_weight.setGeometry(80,80,200,30)
        lbl_weight.setFont(QFont('Times', 12))
            ## solution label
        lbl_solution = QLabel("Solution : ",self)
        lbl_solution.setGeometry(40,170,200,30)
        lbl_solution.setFont(QFont('Times', 12))
            ## Profit label
        lbl_profit = QLabel("      Profit : ",self)
        lbl_profit.setGeometry(41,340,200,30)
        lbl_profit.setFont(QFont('Times', 12))
            ## Time label
        lbl_Time = QLabel("Run Time : ",self)
        lbl_Time.setGeometry(40,370,200,30)
        lbl_Time.setFont(QFont('Times', 12))

        ########## LineEdits #########
            ## weight txt
        self.txt_weight = QLineEdit(self)
        self.txt_weight.setGeometry(240,23,200,25)
        self.txt_weight.setFont(QFont('Times', 10))
            ## population txt
        self.txt_population = QLineEdit(self)
        self.txt_population.setGeometry(240,53,200,25)
        self.txt_population.setFont(QFont('Times', 10))
            ## generation txt
        self.txt_generation = QLineEdit(self)
        self.txt_generation.setGeometry(240,83,200,25)
        self.txt_generation.setFont(QFont('Times', 10))
            ## Solution 
        self.txt_solution = QLineEdit(self)
        self.txt_solution.setEnabled(False)
        self.txt_solution.setGeometry(40,200,400,120)
            ## Profit txt
        self.txt_Profit = QLineEdit(self)
        self.txt_Profit.setEnabled(False)
        self.txt_Profit.setGeometry(150,343,100,25)
        self.txt_Profit.setFont(QFont('Times', 10))
            ## Time txt
        self.txt_Time = QLineEdit(self)
        self.txt_Time.setEnabled(False)
        self.txt_Time.setGeometry(150,373,100,25)
        self.txt_Time.setFont(QFont('Times', 10))

        ########## PushButton #########
        btn = QPushButton("Start",self)
        btn.setGeometry(180,120,100,30)
        btn.clicked.connect(self.on_btn_clicked)
        self.show()

    def on_btn_clicked(self):
        if (self.Check_data() == False):
             QMessageBox.warning(self,'Input Error','Enter Valid Input')
        else:
            # Do main
            Max_iteration= int(self.txt_generation.text())
            Population_Size= int(self.txt_population.text())
            Max_weight= int(self.txt_weight.text())
            solution_array,profit,Ret_time,Profit_arr=Main_Func(Max_iteration,Population_Size,Max_weight)

            self.txt_solution.setText(str(solution_array))
            self.txt_Profit.setText(str(profit))
            self.txt_Time.setText(str(Ret_time))

             # plot
            plt.figure(figsize=(12,8))
            plt.plot(Profit_arr,color='black')
            plt.title('Profit Line Chart')
            plt.xlabel('Iteration')
            plt.ylabel('Max Profit')
            plt.show()


    def Check_data(self):
        try:
            int(self.txt_weight.text())
            int(self.txt_generation.text())
            int(self.txt_population.text())
            return True 
        except:
            return False
        


def main():
    App = QApplication(sys.argv)
    W = Window()
    sys.exit(App.exec_())   

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
    Profit_arr = []
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
        Children_no = int(len(fit_arr))
        parent_no = int(len(population))
        
        selected_child = random.choices(feasible_population,weights=P_array,k=Children_no)
        selected_parent = random.choices(population,k=Children_no)

        population = []
        population = selected_child + selected_parent

        # shffling the population
        random.shuffle(population)

        Tmp_arr = []
        # finding iteration profit
        for person in population:
            Tmp_arr.append(Fitness(person,Max_weight,Data))
        
        Profit_arr.append(max(Tmp_arr))

    # final population:
    fit_arr = []
    for person in population:
            # removing or calculating:
            tmp = Fitness(person,Max_weight,Data)
            fit_arr.append(tmp)

    max_index = fit_arr.index(max(fit_arr))
    return population[max_index],fit_arr[max_index],Profit_arr

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

def Main_Func(Max_iteration,Population_Size,Max_weight):
    global Data
    Data = []

    #Max_iteration,Population_Size,Max_weight= Read_config()


    Read_Data()
    Casting_Data(Data)

    # algorithm
    population = initialization(Data,Population_Size,Max_weight)
    while(True):
        try:
            start =  datetime.now()
            person,profit,Profit_arr = Knapsack(Max_iteration,Max_weight,population,Data)
            RunTime = datetime.now() - start
            break
        except:
            continue

    solution_array = []
    for i in range(len(Data)):
        solution_array.append(0)
    for item in person:
        solution_array[item] = 1
    

    Ret_time = '.'+str(RunTime).split('.')[1]+' sec'
    return solution_array,profit,Ret_time,Profit_arr
    #print('Solution : {}'.format(solution_array))
    #print('Profit : {}'.format(profit))
    #print('Time : {}'.format('.'+str(RunTime).split('.')[1]+' sec'))

if __name__ == '__main__':
    main()
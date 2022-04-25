from audioop import avg
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys 
import re
import csv
from itertools import groupby
import glob
"""
This script plots vertical frequency bars for one bandit experiment.

Give -c as to load the experiment data from .csv files
"""

NUM_BARS = 2
BOUNDS = (0,35)
DIFFERENCE = False
PROPORTIONAL = False
#ideally when generalized, I want two bars to be placed in the 2/6 and 4/6 slots of a plot 
arms = [(5, 1.0), (4, 1.0), (3, 1.0), (2, 1.0), (1, 1.0)] #[(1, 1.0), (2, 1.0), (3, 1.0)]




def arms_rewards_fromCSV(filepath):
    configs = []
    rewards = []
    with open(filepath, newline='') as csvfile:
        utildimser_reader = csv.reader(csvfile)

        next(utildimser_reader)        
        for row in utildimser_reader:

            try:
                #print(row)
                configs.append((int(float(row[3])), round(float(row[2]), 2)))
                rewards.append(float(row[1]))
            except Exception as e:
                print(e)
                print("Exception in file " + filepath)
                print("Row is " + str(row))


    return configs, rewards



num_folders = (int(sys.argv[1]))

folder_names = []
plot_data = []
for i in range(num_folders):
    files = None
    arm_choices = []
    rewards = []
    
    folder = sys.argv[2+i]


    if(folder[-1] != "/"): folder+= "/"

    files = glob.glob(folder + "*.csv")

    folder_names.append(input("Name of boxplot from folder " + str(folder)))

    for j, file in enumerate(files):
        arm, rew = arms_rewards_fromCSV(file)
        bandit_rewards = []
        for i, a in enumerate(arm):
            if(a[1] < 1):
                #print("skipped a cleaning window")
                continue
            else:
                bandit_rewards.append(rew[i])
        #print(bandit_rewards)
        arm_choices.append(arm)
        cum_rew = sum(bandit_rewards)
        print("cumulative reward " + str(j))
        print(cum_rew)
        rewards.append(cum_rew)
    
    plot_data.append(rewards)


plt.boxplot(plot_data)
plt.xticks(ticks=list(range(1,num_folders+1,1)),labels=folder_names)

plt.savefig(input("boxplots name > "))
plt.cla()



            

        
    


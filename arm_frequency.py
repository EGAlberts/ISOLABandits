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
arms = [(3, 1.0), (3, 0.75), (3, 0.5), (3, 0.25), (3, 0.0), (2, 0.0), (2, 0.25), (2, 0.5), (2, 0.75), (2, 1.0), (1, 1.0), (1, 0.75), (1, 0.5), (1, 0.25), (1, 0.0)] #[(1, 1.0), (2, 1.0), (3, 1.0)]




def arms_rewards_fromCSV(filepath):
    configs = []
    rewards = []
    with open(filepath, newline='') as csvfile:
        utildimser_reader = csv.reader(csvfile)

        next(utildimser_reader)        
        for row in utildimser_reader:

            try:
                #print(row)
                configs.append(arms.index((int(float(row[3])), round(float(row[2]), 2))))
                rewards.append(float(row[1]))
            except Exception as e:
                print(e)
                print("Exception in file " + filepath)
                print("Row is " + str(row))


    return configs, rewards

files = None
arm_choices = []
rewards = []
 
if("-c" in sys.argv):
    if("-a" not in sys.argv):
        file = [arg for arg in sys.argv if ".csv" in arg]
        arm, rew = arms_rewards_fromCSV(file)
        arm_choices.extend(arm)
        rewards.extend(rew)

        arm_choices.sort()


        arm_keys = []
        arm_frequency = []

        [(arm_keys.append(str(arms[key])), arm_frequency.append(len(list(group)))) for key, group in groupby(arm_choices)]


        plt.bar(arm_keys, arm_frequency)

        plt.savefig(input("enter plot name > ") + ".png")
    else:
        files = [arg for arg in sys.argv if ".csv" in arg]
        
        if not files:
            folder = sys.argv[-1]
            if(folder[-1] != "/"): folder+= "/"

            files = glob.glob(folder + "*.csv")

        for file in files:
            arm, rew = arms_rewards_fromCSV(file)
            arm_choices.append(arm)
            cum_rew = sum(rew) 
            rewards.append(cum_rew)
        
        frequency_pairs = []
        for arm_choice in arm_choices:
            arm_choice.sort()

            arm_keys = []
            arm_frequency = []
            #print(arm_choice)
            
            [(arm_keys.append(str(arms[key])), arm_frequency.append(len(list(group)))) for key, group in groupby(arm_choice)]


            frequency_pairs.extend([(arm_keys[i], arm_frequency[i]) for i in range(len(arm_keys))])
        
        key_func = lambda x: x[0]
        frequency_pairs.sort(key=key_func)
        averaged_frequencies = [[key, list(group)]  for key, group in groupby(frequency_pairs, key= key_func)]

        plt.figure(1, [20,8])

        for avg_freq in averaged_frequencies:
            
            #x = avg_freq[1]
            for i, item in enumerate(avg_freq[1]):
                avg_freq[1][i] = item[1]

        for avg_freq in averaged_frequencies:
            avg_freq[1] = sum(avg_freq[1]) / len(avg_freq[1])
        
        
        
        arm_keys = []
        arm_frequency = []

        [(arm_keys.append(pair[0]),arm_frequency.append(pair[1])) for pair in averaged_frequencies]


        plt.bar(arm_keys, arm_frequency)

        plt.savefig(input("enter plot name > ") + ".png")



            

        
    

    
else:
    print("give a csv file")
    exit(1)

    #calculate_utility(arrival_rate, dimmer, avg_response_time, max_servers, servers)



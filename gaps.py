from audioop import avg
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys 
import re
import csv
from itertools import groupby
import glob
from statistics import mean, median
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

def truncate(utility, skip):
	if(skip): return utility
	bounds = (300,380)

	lower_bound, upper_bound = bounds

	old_range = upper_bound - lower_bound


	if(utility > upper_bound):
		upper_bound = utility
	elif(utility < lower_bound):
		lower_bound = utility

	new_range = upper_bound - lower_bound

	result = float((utility - lower_bound)/new_range)

	return result



files = None
arm_choices = []
gaps = []
avg_utils = []

folder = sys.argv[1]


if(folder[-1] != "/"): folder+= "/"

files = glob.glob(folder + "*.csv")

for j, file in enumerate(files):
    arm, rew = arms_rewards_fromCSV(file)
    bandit_rewards = []
    current_arm = None
    for i, a in enumerate(arm):
        if(a[1] == 0):
            #print("skipped a cleaning window")
            continue
        else:
            bandit_rewards.append(rew[i])
            current_arm = a

    print("avg normalized is ")
    avg_util = mean([truncate(rew, skip=False) for rew in bandit_rewards])
    print(avg_util)
    print("min is " + str(min(rew)))
    print("max is " + str(max(rew)))

    avg_utils.append((avg_util,current_arm))

best_arm = max(avg_utils, key= lambda k: k[0])
print("avg utils" + str(avg_utils))
for avg_util in avg_utils:
    if avg_util[0] != best_arm[0]:
        gaps.append((best_arm[0] - avg_util[0], avg_util[1]))

print("-----------------")
print("best arm " + str(best_arm))
print("gaps " + str(gaps))
for i, gap in enumerate(gaps):
    print("gap " + str(i))
    print(str(gap))
    print("---")
print("-----------------")




            

        
    


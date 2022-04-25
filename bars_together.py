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
arms = [(3, 1.0), (3, 0.5), (3, 0.0), (2, 0.0), (2, 0.5), (2, 1.0), (1, 1.0), (1, 0.5), (1, 0.0)] #[(1, 1.0), (2, 1.0), (3, 1.0)]
arms.sort()



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




labels = [str(arm) for arm in arms]
num_folders = (int(sys.argv[1]))

freq_data = []
for i in range(num_folders):
    files = None
    arm_choices = []
    rewards = []
    
    folder = sys.argv[2+i]
    if(folder[-1] != "/"): folder+= "/"

    files = glob.glob(folder + "*.csv")

    
    for file in files:
        arm, rew = arms_rewards_fromCSV(file)
        arm_choices.append(arm)

    frequency_pairs = []
    for arm_choice in arm_choices:
        arm_choice.sort()

        arm_keys = []
        arm_frequency = []
            
        [(arm_keys.append(str(arms[key])), arm_frequency.append(len(list(group)))) for key, group in groupby(arm_choice)]

        frequency_pairs.extend([(arm_keys[i], arm_frequency[i]) for i in range(len(arm_keys))])
    
        key_func = lambda x: x[0]
        frequency_pairs.sort(key=key_func)
        averaged_frequencies = [[key, list(group)]  for key, group in groupby(frequency_pairs, key= key_func)]

    for avg_freq in averaged_frequencies:
        for i, item in enumerate(avg_freq[1]):
            avg_freq[1][i] = item[1]

    for avg_freq in averaged_frequencies: avg_freq[1] = round(sum(avg_freq[1]) / len(avg_freq[1]))
    
    arm_keys = []
    arm_frequency = []

    [(arm_keys.append(pair[0]),arm_frequency.append(pair[1])) for pair in averaged_frequencies]

    full_range_data = [0] * len(labels)
    for label_i, label in enumerate(labels):
        if label in arm_keys:
            full_range_data[label_i] = arm_frequency[arm_keys.index(label)]

    freq_data.append(full_range_data)
        

fig, ax = plt.subplots()

x = np.arange(0,3.5*len(labels),3.5)

width = 0.95


bandit1_pos = x - width
bandit2_pos = x
bandit3_pos = x + width

bandit1_means, bandit2_means, bandit3_means = freq_data

bandit1 = ax.bar(bandit1_pos, bandit1_means, width, label='UCB-AO')
bandit2 = ax.bar(bandit2_pos, bandit2_means, width, label='UCB-FH')
bandit3 = ax.bar(bandit3_pos, bandit3_means, width, label='EXP3-FH')

ax.set_ylabel('Arm chosen')
ax.set_xticks(x, labels)
ax.legend()

# ax.bar_label(bandit1, padding=3, label_type="center")
# ax.bar_label(bandit2, padding=3, label_type='center')
# ax.bar_label(bandit3, padding=3, label_type='center')

#fig.tight_layout()

plt.savefig("test3bars.png")



            

        
    


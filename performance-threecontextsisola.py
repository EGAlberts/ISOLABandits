import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys 
import re
import csv
from itertools import groupby
import glob
import collections
from statistics import mean
"""
This script plots vertical frequency bars for one bandit experiment.

Give -c as to load the experiment data from .csv files
"""



NUM_BARS = 2
BOUNDS = (0,35)
DIFFERENCE = False
PROPORTIONAL = False
#ideally when generalized, I want two bars to be placed in the 2/6 and 4/6 slots of a plot 
arms = [(1, 1.0), (2, 1.0), (3, 1.0)] #[(1, 1.0), (2, 1.0), (3, 1.0)]




def parse_server(raw_server):
    received = int(round(float(raw_server)))
    #print("WARNING: This is very ad hoc")
    to_be_returned = received
    if received not in [3,8,13]:
        if(received == 4):
            to_be_returned = 3
        elif(received == 9):
            to_be_returned = 8
    
    if to_be_returned not in [3,8,13]:
        raise RuntimeError("Unexpected server value(s)")

    return to_be_returned



def arms_rewards_fromCSV(filepath, time_boundary):
    configs = []
    rewards = []
    start_time = time_boundary[0]
    end_time = time_boundary[1]
    with open(filepath, newline='') as csvfile:
        utildimser_reader = csv.reader(csvfile)

        next(utildimser_reader)        
        for row in utildimser_reader:
            time_stamp = int(row[0])
            if(time_stamp < end_time and time_stamp > start_time):
                try:
                    configs.append((parse_server(row[3]), round(float(row[2]), 2)))
                    rewards.append(float(row[1]))
                except Exception as e:
                    print(e)
                    print("Exception in file " + filepath)
                    print("Row is " + str(row))


    return configs, rewards




num_folders = (int(sys.argv[1]))

if num_folders == 0:
    loc_folder = input("directory to grab all folders from > ")
    all_folders = glob.glob(loc_folder + "*/")
    num_folders = len(all_folders)
else:
    all_folders = sys.argv[2:(2+num_folders)]


folder_names = []
plot_data = {}

#num_contexts = int(input("How many different contexts are there? > "))
#base(140,14900) traffic_change(110,100) traffic_steady(14900) traffic_change(140, 100) traffic_steady(15000)

shift_moment_one = int(input("when is shift 1 ? e.g. 14925 > "))
shift_moment_two = int(input("when is shift 2 ? e.g. 14925 > "))

context_boundaries = [(0,shift_moment_one), (shift_moment_one,shift_moment_two), (shift_moment_two, 9999999)] #[(0,5075), (5075,9999999)]

best_arm_input1 = input("best arm context 1: e.g. 10,1.0 >").split(',')
best_arm1 = (int(best_arm_input1[0]),float(best_arm_input1[1]))

best_arm_input2 = input("best arm context 2: e.g. 5,1.0 >").split(',')
best_arm2 = (int(best_arm_input2[0]),float(best_arm_input2[1]))

best_arm_input3 = input("best arm context 3: e.g. 5,1.0 >").split(',')
best_arm3 = (int(best_arm_input3[0]),float(best_arm_input3[1]))

best_arms = [best_arm1, best_arm2, best_arm3]

# for i in range(1,num_contexts,1):
#     context_boundaries.append(int(input("At what point does context " + str(i) + " begin? > ")))
#     best_arm_input = input("What is the best arm for context " + str(i) + ": e.g. 4,1.0 >").split(',')
#     best_arm = (int(best_arm_input[0]),float(best_arm_input[1]))
#     best_arms.append(best_arm)


for cntxt_bnd in context_boundaries:
    plot_data[cntxt_bnd] = {}

for i in range(num_folders):
    files = None
    arm_choices = []
    rewards = []
    
    folder = all_folders[i]


    if(folder[-1] != "/"): folder+= "/"

    files = glob.glob(folder + "*.csv")

    folder_names.append(input("Name of line from folder " + str(folder)))
    curr_folder = folder_names[-1]
    
    
    for c_i, context_boundary in enumerate(context_boundaries):
        best_arm = best_arms[c_i]
        bandit_rounds = []
        all_bandit_arms = []
        rewards_for_run = []
        for j, filee in enumerate(files):
            arm, rew = arms_rewards_fromCSV(filee, context_boundary) #all the arms from run i
            bandit_rewards = []
            bandit_arms = []

            for i, a in enumerate(arm):
                if(a[1] < 1):
                    #print("skipped a cleaning window")
                    continue
                else:
                    #print("this happened")
                    bandit_arms.append(a)
                    bandit_rewards.append(rew[i])

            #print(bandit_rewards)

            #print(bandit_arms)
            #xit(0)
            all_bandit_arms.append(bandit_arms)
            bandit_rounds.append(len(bandit_rewards))
            rewards_for_run.append(bandit_rewards)

        least_rounds = min(bandit_rounds)
 
        averaged_reward_per_rounds = [0] * least_rounds
        for i, run_rewards in enumerate(rewards_for_run):
            current_run = run_rewards
            for j in range(len(averaged_reward_per_rounds)):
                averaged_reward_per_rounds[j]+= current_run[j]
        
        for i, rew_sum in enumerate(averaged_reward_per_rounds): averaged_reward_per_rounds[i] = rew_sum/30


        plot_data[context_boundary][curr_folder] = averaged_reward_per_rounds



print("plot data")
print(plot_data)

#[print(len(plot_data[context_boundaries[0]][fol_name])) for fol_name in folder_names]



fig, axs = plt.subplots(1, 3)
#colors = ['k', 'c', 'm', 'b']
plt.style.use('seaborn-bright')
for c_i, context_boundary in enumerate(context_boundaries):
    curr_ax = axs[c_i]

    current_plot_data = plot_data[context_boundary]

    context_values = []

    for key in current_plot_data.keys():
        context_values = context_values + current_plot_data[key]
        print(str(key) + "has length " + str(len(current_plot_data[key])))
    # print("The shortest run is " + str(len(min(current_plot_data.keys, key = lambda k: len(k)))))

    context_mean = mean(context_values)

    shortest_rounds = int(input("How many rounds should the plot include? > "))

    
    for i, key in enumerate(current_plot_data.keys()):
        performance_relative_to_mean = [(value-context_mean)/value for value in current_plot_data[key][0:shortest_rounds]]
        curr_ax.plot(current_plot_data[key][0:shortest_rounds], alpha = 0.5, label=(folder_names[i] + " " + str(round(sum(performance_relative_to_mean)))))
        last_bad = 0


        #print((last_bad,0.0,convergence_boundary, colors[i], 'dashed','Conv. Point ' + folder_names[i] ))

    #longest = len(max(plot_data, key = lambda k: len(k)))

    curr_ax.legend(fontsize='small', loc='lower right')
    #curr_ax.xlabel('bandit rounds')
    #curr_ax.ylabel('convergence factor')
    #curr_ax.xticks(np.arange(0,shortest_rounds+1,3))
all_y_ticks = []
for ax in axs: 
    all_y_ticks.append([float(tick) for tick in list(ax.get_yticks())])

for ax in axs.flat:
    ax.set_xlabel('rounds', fontdict={'size': 14})
    ax.set_ylabel('reward', fontdict={'size': 14})

all_y_ticks.sort(key= lambda ticklist: ticklist[-1]-ticklist[0])

print(all_y_ticks)

print(all_y_ticks[-1])

print(type(all_y_ticks[-1][0]))

for ax in axs: 
    ax.set_yticks(all_y_ticks[-1])
plt.tight_layout()
plt.savefig(input("plot name > ") + ".pdf")




            

        
    


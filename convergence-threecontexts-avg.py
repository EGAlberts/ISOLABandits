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

print(all_folders)
folder_names = []
plot_data = {}

#num_contexts = int(input("How many different contexts are there? > "))

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


length_dictionary = {}
for i in range(num_folders): #policy loop
    files = None
    arm_choices = []
    rewards = []
    
    folder = all_folders[i]


    if(folder[-1] != "/"): folder+= "/"

    files = glob.glob(folder + "*.csv")

    folder_names.append(folder.split("/")[-2])
    curr_folder = folder_names[-1]
    
    length_dictionary[curr_folder] = 0
    for c_i, context_boundary in enumerate(context_boundaries): #contexts loop

        best_arm = best_arms[c_i]
        bandit_rounds = []
        all_bandit_arms = []

        for j, filee in enumerate(files): #runs
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



        #ratio of the best arm being chosen within this given context, averaged over the 30 runs.
        least_rounds = min(bandit_rounds)
        plot_data[context_boundary][curr_folder] = (all_bandit_arms,least_rounds)

table_data = {}
for cntxt_bnd in context_boundaries:
    table_data[cntxt_bnd] = {}

for c_i, context_boundary in enumerate(context_boundaries): #contexts loop
    current_plot_data = plot_data[context_boundary]
    all_context_rounds = []
    best_arm = best_arms[c_i]
    for i, policy in enumerate(current_plot_data.keys()): #for each policy
        _, p_least_rounds = current_plot_data[policy] 
        all_context_rounds.append(p_least_rounds)
    for i, policy in enumerate(current_plot_data.keys()): #for each policy
        p_bandit_arms, p_least_rounds = current_plot_data[policy] 
        least_across_all = min(all_context_rounds)

        ratio_over_runs = []
        choices_over_runs = []
        for k in range(len(p_bandit_arms)): #30 runs
            choices_made_in_run = p_bandit_arms[k][0:least_across_all] #all arms chosen in this given context
            opt_freq = float(collections.Counter(choices_made_in_run)[best_arm])/len(choices_made_in_run) #convergence ratio
            ratio_over_runs.append(opt_freq)
            choices_over_runs.append(len(choices_made_in_run))
        ratio_over_context = mean(ratio_over_runs)
        choices_over_context = mean(choices_over_runs) #redundant with min(all_context_rounds) but sure
        
        table_data[context_boundary][policy] = (ratio_over_context,choices_over_context)

    

table_headers = ["Context 1", "Context 2", "Context 3 ", "Simple Average", "Weighted Average"]
table_rows = ["Average Convergence"]
# context_stuff = []
# average_over_all = {}
# for c_i, context_boundary in enumerate(context_boundaries):

#     current_plot_data = plot_data[context_boundary]

    
#     # print("The shortest run is " + str(len(min(current_plot_data.keys, key = lambda k: len(k)))))

#     shortest_rounds = min([len(current_plot_data[key]) for key in current_plot_data.keys()])

#     for i, key in enumerate(current_plot_data.keys()): #for each policy

#         current_plot_data[key] = round(mean(current_plot_data[key][0:shortest_rounds]),3)
        
#         last_bad = 0

#     #longest = len(max(plot_data, key = lambda k: len(k)))
#     context_stuff.append(current_plot_data)


d = {}
for i, key in enumerate(table_data[context_boundaries[0]].keys()):    
    d[key] = [table_data[context_boundaries[0]][key][0],table_data[context_boundaries[1]][key][0], table_data[context_boundaries[2]][key][0], mean([table_data[context_boundaries[0]][key][0],table_data[context_boundaries[1]][key][0], table_data[context_boundaries[2]][key][0]]),  \
    np.average([table_data[context_boundaries[0]][key][0],table_data[context_boundaries[1]][key][0], table_data[context_boundaries[2]][key][0]], weights=[table_data[context_boundaries[0]][key][1],table_data[context_boundaries[1]][key][1], table_data[context_boundaries[2]][key][1]])]

print ("{:<40} {:<10} {:<10} {:<10} {:<20} {:<20}".format('Policy', 'Context 1','Context 2', 'Context 3', 'Simple Average', 'Weighted Average'))

table_items = [(k,v) for k, v, in d.items()]

table_items.sort(key= lambda x: x[-1][-1])


#print(table_items)

for k, v in table_items:
    c1mean, c2mean, c3mean, simplemean, weightmean = v
    print("{:<40} {:<10} {:<10} {:<10} {:<20} {:<20}".format(k, round(c1mean,2), round(c2mean,2), round(c3mean,2),  round(simplemean,2), round(weightmean,2)))




            

        
    


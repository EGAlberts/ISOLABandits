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
                    configs.append((int(float(row[3])), round(float(row[2]), 2)))
                    rewards.append(float(row[1]))
                except Exception as e:
                    print(e)
                    print("Exception in file " + filepath)
                    print("Row is " + str(row))


    return configs, rewards



num_folders = (int(sys.argv[1]))

folder_names = []
plot_data = {}

#num_contexts = int(input("How many different contexts are there? > "))

cnt_border = int(input("context border > "))
context_boundaries = [(0, cnt_border), (cnt_border,9999999)] #[(0,5075), (5075,9999999)]

best_arm1 = input("best arm 1 > ").split(',')
best_arm1 = (int(best_arm1[0]), float(best_arm1[1]))

best_arm2 = input("best arm 2 > ").split(',')
best_arm2 = (int(best_arm2[0]), float(best_arm2[1]))
best_arms = [best_arm1, best_arm2]


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
    
    folder = sys.argv[2+i]


    if(folder[-1] != "/"): folder+= "/"

    files = glob.glob(folder + "*.csv")

    folder_names.append(input("Name of line from folder " + str(folder)))
    curr_folder = folder_names[-1]
    
    
    for c_i, context_boundary in enumerate(context_boundaries):
        best_arm = best_arms[c_i]
        bandit_rounds = []
        all_bandit_arms = []
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

        # print(all_bandit_arms)
        # print(bandit_rounds)


        least_rounds = min(bandit_rounds)



    
        convergence_ratio = []
        phase_len = 5

        total_bandit_rounds = least_rounds

        #context 0: 0 until rounds_per_context[0], prev+1 until rounds_per_context[1]


        for b_round in range(0,least_rounds-(phase_len-1),phase_len):
            ratio_in_phase = []
            for k in range(len(files)): #30 runs

                #print(k)
                phase_choices = all_bandit_arms[k][b_round:b_round+phase_len]
                opt_freq = float(collections.Counter(phase_choices)[best_arm])/len(phase_choices)
                ratio_in_phase.append(opt_freq)
            #print("ratio in phase")
            #print(ratio_in_phase)
            convergence_ratio.append(mean(ratio_in_phase))
            
        #print(convergence_ratio)
        plot_data[context_boundary][curr_folder] = convergence_ratio

print("plot data")
print(plot_data)

[print(len(plot_data[context_boundaries[0]][fol_name])) for fol_name in folder_names]


convergence_boundary = float(input("convergence boundary > "))
plt.style.use('seaborn-bright')
#colors = ['k', 'c', 'm', 'b']


fig, axs = plt.subplots(1, 2)

for c_i, context_boundary in enumerate(context_boundaries):
    curr_ax = axs[c_i]

    current_plot_data = plot_data[context_boundary]

    for key in current_plot_data.keys():
        print(str(key) + "has length " + str(len(current_plot_data[key])))
    # print("The shortest run is " + str(len(min(current_plot_data.keys, key = lambda k: len(k)))))

    shortest_rounds = int(input("How many rounds should the plot include? > "))


    for i, key in enumerate(current_plot_data.keys()):

        curr_ax.plot(current_plot_data[key][0:shortest_rounds], alpha=0.5, label=folder_names[i] + " - " + str(round(mean(current_plot_data[key][0:shortest_rounds]),2)))
        last_bad = 0
        for j, phasum in enumerate(current_plot_data[key]):
            if phasum <= convergence_boundary:
                last_bad = j
        print("--brr---")
        print(last_bad)
        print(shortest_rounds)
        if(last_bad < (shortest_rounds-1)):
            pass
            #curr_ax.vlines(last_bad,0.0,convergence_boundary, linestyles='dashed',label='Conv. Point ' + folder_names[i] )

        #print((last_bad,0.0,convergence_boundary, colors[i], 'dashed','Conv. Point ' + folder_names[i] ))

    #longest = len(max(plot_data, key = lambda k: len(k)))

    curr_ax.hlines(convergence_boundary, 0, shortest_rounds-1, color ='black', label='conv. boundary')
    curr_ax.legend(fontsize='medium', title="policy - mean conv. factor") #loc='lower right'
    #curr_ax.xlabel('bandit rounds')
    #curr_ax.ylabel('convergence factor')
    #curr_ax.xticks(np.arange(0,shortest_rounds+1,3))

for ax in axs.flat:
    ax.set_xlabel('phases (length=' + str(phase_len)+"rounds)", fontdict={"size":14})
    ax.set_ylabel('convergence factor', fontdict={'size': 14})


all_y_ticks = []
all_x_ticks = []
for ax in axs: 
    all_y_ticks.append([float(tick) for tick in list(ax.get_yticks())])
    all_x_ticks.append([float(tick) for tick in list(ax.get_xticks())])

print(all_x_ticks)

x_steps = [ticklist[1] - ticklist[0] for ticklist in all_x_ticks]

x_steps.sort()
smallest_x_step = x_steps[0]
print(smallest_x_step)
all_y_ticks.sort(key= lambda ticklist: ticklist[-1]-ticklist[0])
all_x_ticks.sort(key= lambda ticklist: ticklist[-1]-ticklist[0], reverse=True)


for ax in axs: 
    ax.set_yticks(all_y_ticks[-1])
    left, right = ax.get_xlim()
    print(np.arange(left,right,smallest_x_step))
    #ax.set_xticks(np.arange(left,right,smallest_x_step))

plt.tight_layout()
plt.savefig(input("plot name > ") + ".pdf")




            

        
    


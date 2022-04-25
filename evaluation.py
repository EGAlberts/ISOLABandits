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




def arms_rewards_fromCSV(filepath):
    configs = []
    rewards = []
    times = []
    with open(filepath, newline='') as csvfile:
        utildimser_reader = csv.reader(csvfile)

        next(utildimser_reader)        
        for row in utildimser_reader:

            try:
                #print(row)
                times.append(int(row[0]))
                configs.append((int(float(row[3])), round(float(row[2]), 2)))
                rewards.append(float(row[1]))
            except Exception as e:
                print(e)
                print("Exception in file " + filepath)
                print("Row is " + str(row))


    return configs, rewards, times



num_folders = (int(sys.argv[1]))

folder_names = []
plot_data = []
plot_data2 = []

if num_folders == 0:
    loc_folder = input("directory to grab all folders from > ")
    all_folders = glob.glob(loc_folder + "*/")
    num_folders = len(all_folders)
else:
    all_folders = sys.argv[2:(2+num_folders)]

for i in range(num_folders):
    files = None
    arm_choices = []
    rewards = []
    
    folder = all_folders[i]


    if(folder[-1] != "/"): folder+= "/"

    files = glob.glob(folder + "*.csv")

    folder_names.append(folder.split("/")[-2].split("\\")[-2])
    #folder_names.append(input("Name of line from folder " + str(folder)))
    bandit_rounds = []
    all_bandit_arms = []
    alg_times = {}
    max_per_time = {}
    for j, filee in enumerate(files):
        arm, rew, times = arms_rewards_fromCSV(filee) #all the arms from run i
        bandit_rewards = []
        bandit_arms = []
        #for time_s in times: alg_times[time_s] = []
        for i, a in enumerate(arm):
            if(a[1] == 0):
                #print("skipped a cleaning window")
                continue
            else:
                #print("this happened")
                if(times[i] not in alg_times): alg_times[times[i]] = []
                alg_times[times[i]].append(rew[i])
                
                bandit_arms.append(a)
                bandit_rewards.append(rew[i])
        #print(bandit_rewards)

        #print(bandit_arms)
        #xit(0)
        all_bandit_arms.append(bandit_arms)
        bandit_rounds.append(len(bandit_rewards))
    

    least_rounds = min(bandit_rounds)
    print(alg_times)
    for key in alg_times.keys():
        print(alg_times[key])
        if(alg_times[key] != []):
            max_per_time[key] = max(alg_times[key])
            alg_times[key] = mean(alg_times[key])
            
        else:
            alg_times[key] = 0
            max_per_time[key] = 0


    plot_data.append(alg_times)
    plot_data2.append(max_per_time)

#print(plot_data)
#exit(0)
plt.style.use('seaborn-bright')
#cm = plt.get_cmap('viridis')
#colors = cm.colors#['k', 'c', 'm', 'b']

#plt.cycler('color', cm.colors)

print("plot_data")
print(plot_data)


plot_data = plot_data2


actually_gonna_plot = []
cumulative_utils = []
mapping_cum_to_index = {}
for i, datum in enumerate(plot_data):
    key_list = list(datum.keys())
    key_list.sort()
    sorted_events = [datum[tstamp] for tstamp in key_list]
    cumulative_utils.append(sum(sorted_events))
    mapping_cum_to_index[sum(sorted_events)] = i

cumulative_utils.sort()

top_4 = cumulative_utils[-4:]

for c_util in top_4:
    actually_gonna_plot.append(mapping_cum_to_index[c_util])

for index_plot in actually_gonna_plot:
    datum = plot_data[index_plot]
    key_list = list(datum.keys())
    key_list.sort()
    sorted_events = [datum[tstamp] for tstamp in key_list]

    plt.plot(key_list, sorted_events, label=folder_names[index_plot]+ " " + str(round(sum(sorted_events)))) #color = matplotlib.colors.to_rgba(colors[i], 0.5)

   
    #print((last_bad,0.0,convergence_boundary, colors[i], 'dashed','Conv. Point ' + folder_names[i] ))


#longest = len(max(plot_data, key = lambda k: len(k)))


plt.legend(fontsize='small', loc='lower right')
plt.xlabel('rounds', fontdict={"size": 14})
plt.ylabel('utility', fontdict={"size": 14})
#plt.xticks(np.arange(0,shortest_rounds+1,3))
plt.savefig(input("plot name > ") + ".pdf")
plt.cla()



            

        
    


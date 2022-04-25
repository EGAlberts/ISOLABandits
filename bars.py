import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys 
import re
import csv
"""
This script plots horizontal convergence bars for two sources of bandit experiments.
There is an option -d to show the difference between the two bars between them.
There is an option -p which makes the size of bar segments be proportional to their payoff/reward.
Then you can choose either option -f | -c as to whether you are loading the experiment data from .txt files or .csv files
"""

NUM_BARS = 2
BOUNDS = (0,35)
DIFFERENCE = False
PROPORTIONAL = False
#ideally when generalized, I want two bars to be placed in the 2/6 and 4/6 slots of a plot 
arms = [(5, 1.0), (5, 0.75), (5, 0.5), (5, 0.25), (5, 0.0),(4, 1.0), (4, 0.75), (4, 0.5), (4, 0.25), (4, 0.0),(3, 1.0), (3, 0.75), (3, 0.5), (3, 0.25), (3, 0.0), (2, 0.0), (2, 0.25), (2, 0.5), (2, 0.75), (2, 1.0), (1, 1.0), (1, 0.75), (1, 0.5), (1, 0.25), (1, 0.0)] #[(1, 1.0), (2, 1.0), (3, 1.0)]

def truncate(utility):
    global BOUNDS
    bounds_tuple = BOUNDS
    
    lower_bound = bounds_tuple[0]
    upper_bound = bounds_tuple[1]

    x = utility

    if(x > upper_bound):
        x = upper_bound
    elif(x < lower_bound):
        x = lower_bound

    x = x + abs(lower_bound)
    result = float(x/(upper_bound + abs(lower_bound)))

    return result

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

    #print(configs)
    #print(rewards)
    return configs, rewards

def coloring(arms):
    final_colors = {}
    colormaps = [plt.cm.Greys, plt.cm.Purples, plt.cm.Greens, plt.cm.Oranges, plt.cm.Reds]

    unique_servers = np.unique([arm[0] for arm in arms])
    unique_dimmers = np.unique([arm[1] for arm in arms])

    unique_servers.sort()
    unique_dimmers.sort()

    for u_server in unique_servers:
        c_map = colormaps[u_server-1](np.linspace(0, 1, len(unique_dimmers) + 1)) #0.0 was too light, so I am offsetting it by 1

        for i_dimmer in range(len(unique_dimmers)):
            final_colors[(u_server,unique_dimmers[i_dimmer])] = c_map[i_dimmer + 1] #offset here f or consistency with above comment

    return final_colors


coloring_map = coloring(arms)
#print(str(coloring_map))
arm_choices = None
arm_choices2 = None

rewards = None
rewards2 = None

files = None
arm_choices = []
rewards = []

if("-f" in sys.argv):
    files = [arg for arg in sys.argv if ".txt" in arg]
    
    # if(len(files) > 2): raise RuntimeError("too many .txt files provided")

    for file in files:
        f = open(file)
        arm_choices.append([int(x) for x in f.readline().split()])
        rewards.append([float(x) for x in f.readline().split()])
        f.close()

    

    
    
elif("-c" in sys.argv):
    files = [arg for arg in sys.argv if ".csv" in arg]
    
    #if(len(files) != 2): raise RuntimeError("Either too few or too many .csv files provided")

    for file in files:
        arm, rew = arms_rewards_fromCSV(file)
        arm_choices.append(arm)
        rewards.append(rew)
   


    #calculate_utility(arrival_rate, dimmer, avg_response_time, max_servers, servers)


if("-d" in sys.argv): DIFFERENCE = True #adds a bar which shows where they're different
if("-p" in sys.argv): PROPORTIONAL = True #makes it so that segment height reflects reward


    

algorithms = tuple(files)


all_armchoices = []
[all_armchoices.extend(a_c) for a_c in arm_choices]

unique_arms = list(set(all_armchoices))

number_of_arms = len(unique_arms)

#colors = plt.cm.rainbow(np.linspace(0, 1, number_of_arms))
#here is a list of spectrums you can choose from https://matplotlib.org/stable/tutorials/colors/colormaps.html, the np.linspace divides the spectrum evenly into <num_arms> colors.


fig, axs = plt.subplots()

y_positions = [0.66]

for bar_i in range(len(files)-1):
    next = y_positions[-1] + 0.66
    y_positions.append(next)



for i in range(len(arm_choices)):
    arm_choice = arm_choices[i]
    reward = rewards[i]
    pos = 0

    if(len(reward) != len(arm_choice)):
        raise RuntimeError("The number of rewards and configurations chosen does not match for data source " + str(files[i]) + "remove -p option to ignore this and only plot configurations")

    for choice in arm_choice: #use left to determine where the bar segment will start
        h = axs.barh(y=y_positions[i], width=1, left = pos, height = (reward[pos] * 0.15) if PROPORTIONAL else 0.15, color = coloring_map[arms[choice]])
        pos = pos + 1

# pos = 0
# for choice in arm_choices2: #use left to determine where the bar segment will start
#     axs.barh(y=1.33, width=1, left = pos, height = (rewards2[pos] * 0.15) if PROPORTIONAL else 0.15, color = coloring_map[arms[choice]])
#     pos = pos + 1


if(DIFFERENCE):
    for i in range(len(arm_choices)-1):
        #list of arm indices
        compareto = arm_choices[i] #the nth bar chart
        comparewith = arm_choices[i+1] #and the n+1th bart chart to find differences with
        pos = 0
        for j in range(len(compareto)): #for each choice
            match = "white"
            if(compareto[j] != comparewith[j]): match = "black"
            h = axs.barh(y=y_positions[i]+0.33, width=1, left = pos, height = 0.15, color = match)

            pos = pos + 1


axs.set_yticks(y_positions)
axs.set_yticklabels(algorithms)

locs, labels = plt.yticks()

plt.ylim([0,y_positions[-1] + 0.66])


#manually make the legend
handles = [ matplotlib.patches.Patch(color=coloring_map[arms[i]], label = str(arms[i])) for i in unique_arms ]
plt.legend(handles = handles, loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=5)
    


plt.xlabel("Exploited")

plt.savefig(input("plot name? > ") + ".png")





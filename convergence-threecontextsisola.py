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




def print_list_indices(list_to_print):
    for i, item in enumerate(list_to_print):
        print("%i: %s" % (i, item))


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


res_path = input("Enter the path to the results > ")
res_folders = glob.glob(res_path + "*/")
print_list_indices(res_folders)
setting_indices = [int(i) for i in input("Which settings (by index) should be plotted > ").split(" ")]

# number_of_plots = len(setting_indices)
# if(number_of_plots == 1):
#     fig, axs = plt.subplots()
# elif(number_of_plots == 2):
#     fig, axs = plt.subplots(number_of_plots)
# elif(number_of_plots == 3):
#     fig, axs = plt.subplots()    
    
for setting_index in setting_indices:
    
    policy_folders = glob.glob(res_folders[setting_index] + "*/")
    print_list_indices(policy_folders)
    policy_indices = [int(i) for i in input("Which policies (by index) should be plotted > ").split(" ")]

    all_folders = [policy_folders[policy_index] for policy_index in policy_indices]
    num_folders = len(all_folders)
    phase_len = int(input("phase len > "))



# num_folders = (int(sys.argv[1]))

# if num_folders == 0:
#     loc_folder = input("directory to grab all folders from > ")
#     all_folders = glob.glob(loc_folder + "*/")
#     num_folders = len(all_folders)
# else:
#     all_folders = sys.argv[2:(2+num_folders)]

# print(all_folders)
    folder_names = []
    plot_data = {}

    if("XXY" in res_folders[setting_index]):
        shift_moment_one = 7201
        shift_moment_two = 13921
    elif("XYY" in res_folders[setting_index]):
        shift_moment_one = 7201
        shift_moment_two = 8521
    elif("YXY" in res_folders[setting_index]):
        shift_moment_one = 1801
        shift_moment_two = 8521

    # shift_moment_one = int(input("when is shift 1 ? e.g. 14925 > "))
    # shift_moment_two = int(input("when is shift 2 ? e.g. 14925 > "))

    context_boundaries = [(0,shift_moment_one), (shift_moment_one,shift_moment_two), (shift_moment_two, 9999999)] #[(0,5075), (5075,9999999)]

    #best_arm_input1 = input("best arm context 1: e.g. 10,1.0 >").split(',')
    best_arm1 = (3,1.0)#(int(best_arm_input1[0]),float(best_arm_input1[1]))

    #best_arm_input2 = input("best arm context 2: e.g. 5,1.0 >").split(',')
    best_arm2 = (8,1.0)#(int(best_arm_input2[0]),float(best_arm_input2[1]))

    #best_arm_input3 = input("best arm context 3: e.g. 5,1.0 >").split(',')
    best_arm3 = (3,1.0)#(int(best_arm_input3[0]),float(best_arm_input3[1]))

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
            context_ratios = []
            p_bandit_arms, _ = current_plot_data[policy] 
            least_across_all = min(all_context_rounds)

            ratio_over_runs = []
            choices_over_runs = []

            
            # choices_made_in_run = p_bandit_arms[k][0:least_across_all] #all arms chosen in this given context
            for b_round in range(0,least_across_all-(phase_len-1),phase_len):
                ratio_in_phase = []
                for run_i in range(len(p_bandit_arms)): #30 runs

                    phase_choices = p_bandit_arms[run_i][b_round:b_round+phase_len]
                    opt_freq = float(collections.Counter(phase_choices)[best_arm])/len(phase_choices)
                    ratio_in_phase.append(opt_freq)
                #print("ratio in phase")
                #print(ratio_in_phase)
                context_ratios.append(mean(ratio_in_phase))
            
            table_data[context_boundary][policy] = context_ratios

    plt.style.use('seaborn-bright')

    plot_lines = []
    #fig, axs = plt.subplots(1, 2)

    policies = {}
    for c_i, context_boundary in enumerate(context_boundaries): #contexts loop
        current_plot_data = table_data[context_boundary]
        for i, policy in enumerate(current_plot_data.keys()): #for each policy
            policies[policy] = []

    boundary_coords = [0]
    for c_i, context_boundary in enumerate(context_boundaries): #contexts loop
        current_plot_data = table_data[context_boundary]
        boundary_coords.append((boundary_coords[-1] + len(current_plot_data[list(current_plot_data.keys())[0]])))


        for i, policy in enumerate(current_plot_data.keys()): #for each policy
            policies[policy].extend(current_plot_data[policy])

    boundary_coords = list(set(boundary_coords))

    boundary_coords.sort()
    boundary_coords.pop(0)
    boundary_coords.sort()
    boundary_coords.pop(-1)



    print(boundary_coords)




    for i, key in enumerate(policies.keys()):
        plt.plot(policies[key], alpha=0.8, label=folder_names[i].split("\\")[-2])
        # last_bad = 0
        # for j, phasum in enumerate(current_plot_data[key]):
        #     if phasum <= convergence_boundary:
        # #         last_bad = j
        # print("--brr---")
        # print(last_bad)
        # print(shortest_rounds)
        # if(last_bad < (shortest_rounds-1)):
        #     pass

    for coord in boundary_coords:
        plt.vlines(coord,0,1.0,'black','dashed')
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.xlabel('phases (length=' + str(phase_len)+" rounds)", fontdict={"size":18})
    plt.ylabel('convergence factor', fontdict={'size': 18})
    if('y' in input("legend? y/n")): plt.legend(prop={"size":14})
    plt.tight_layout()
    plt.savefig(input("plot name > ") + ".pdf")
    plt.cla()

        
    


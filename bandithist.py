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


 
arms = [(1, 1.0), (2, 1.0), (3, 1.0)] #[(1, 1.0), (2, 1.0), (3, 1.0)]


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


durr = []
for noise in ["1", "3"]:
    for expID in ["4to10", "1to3"]:
        durr.append("results/noisyarms/noisy/" + expID + "/" + noise + "/")





files = None
arm_choices = []
rewards = []

#folder = sys.argv[1]


#if(folder[-1] != "/"): folder+= "/"

for folder in durr: 
    pltnames = []
    files = glob.glob(folder + "*.csv")

    bandit_rounds = []
    all_bandit_arms = []
    all_bandit_rews = []
    for j, filee in enumerate(files):
        pltnames.append(input("Name of file from folder " + str(filee) + "> "))
        if(pltnames[-1] == "skip"): continue
        arm, rew = arms_rewards_fromCSV(filee) #all the arms from run i
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
        all_bandit_rews.append(bandit_rewards)
        all_bandit_arms.append(bandit_arms)
        bandit_rounds.append(len(bandit_rewards))
        


    plt.style.use('seaborn-bright')


    alphachosen = 0.5 #float(input("transparency of bars > "))
    for i, datum in enumerate(all_bandit_rews):
        plt.hist(datum, alpha = alphachosen, label=pltnames[i], histtype = 'stepfilled')


    #longest = len(max(plot_data, key = lambda k: len(k)))

    plt.legend(fontsize='medium', loc='lower right')
    plt.xlabel('reward', fontdict={"size":14})
    plt.ylabel('frequency', fontdict={"size":14})
    plt.tight_layout()
    plt.savefig(folder + "histfinal.pdf")#input("plot name > ") + ".pdf")
    plt.cla()



            

        
    


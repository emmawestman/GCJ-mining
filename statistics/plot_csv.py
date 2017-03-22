import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas


gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *


def plot_feature(x,y,p_id,feature):
    languages = get_LANGUAGE()
    plt.yticks(range(len(languages)),languages)
    plt.scatter(x,y, label= feature + ' ' + p_id)
    plt.xlabel(feature)
    plt.ylabel('Language')
    plt.title('Interesting Graph\nCheck it out!')
    plt.legend()
    plt.show()


def plot_cloc():
    for p_id in get_PROBLEM_IDS(gcj_path):
        for x in range(0,1):
            path_to_cloc = os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',p_id+'.csv'))
            x = []
            y = []
            languages = get_LANGUAGE()
            with open(path_to_cloc,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter=',')
                first_row = next(plots, None)  # skip the headers
                cloc_index = first_row.index('cloc')
                languages_index = first_row.index('language')
                for row in plots:
                    if len(row)>0 :
                        x.append(int(row[cloc_index]))
                        y.append(languages.index(row[languages_index]))
                plot_feature(x,y,p_id,'cloc')

def plot_max_ram():
    for p_id in get_PROBLEM_IDS(gcj_path):
        for x in range(0,1):
            path_to_cloc = os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',p_id+'.csv'))
            x = []
            y = []
            languages = get_LANGUAGE()
            with open(path_to_cloc,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter=',')
                first_row = next(plots, None)  # skip the headers
                max_RAM_index = first_row.index('max_RAM')
                languages_index = first_row.index('language')
                for row in plots:
                    if len(row)>0 :
                        if row[max_RAM_index] != '-':
                            x.append(int(row[max_RAM_index]))
                            y.append(languages.index(row[languages_index]))
                plot_feature(x,y,p_id,'max_ram')



def plot_rank_language():
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')

    for contest_id in get_CONTEST_IDS():
        d1 = pandas.read_csv(os.path.join(get_GCJ_BACKUP_PATH(),contest_id+'.csv'),sep=',')
        temp_list = []

        #create frames for every problem and select columns 'user_id ,language,penalty'
        for problem_id in dict_cid_to_pid[contest_id]:
            for x in ['0','1']:
                path_to_csv = os.path.join(get_GCJ_BACKUP_PATH(),problem_id + '_' + x +'.csv')
                if os.path.isfile(path_to_csv):
                    d2 = pandas.read_csv(path_to_csv)
                    df = pandas.merge(d1, d2, on = 'user_id')
                    temp=df[['user_id','language','penalty']]
                    temp_list.append(temp)

        # merge tables for all problemes into one
        test = temp_list[0]
        for intem in range(1,len(temp_list)):
            test = pandas.merge(test,temp_list[intem])

        plt.figure()
        test.boxplot(column=['user_id','penalty'], by=['language'])
        plt.show();
        #group by language and plot
        #for key, grp in test.groupby(['language']):

            #grp.plot(x=users,y='penalty',kind='scatter',label = key)

        #plt.show()




plot_rank_language()

import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas
<<<<<<< HEAD

=======
>>>>>>> missingMainC++

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *


def plot_rank_language():
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    #create frame for contest csv
    for contest_id in get_CONTEST_IDS():
        print "CONTEST ID " + contest_id
        contest_dict = pandas.read_csv(os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',contest_id+'.csv')))

        #this is needed in order to merge all problem_ids
        list_of_frames=[]

        #create frames for every problem and select columns 'user_id ,language,penalty'

        problem_id = dict_cid_to_pid[contest_id][0]
        path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(),problem_id + '_0' +'.csv'))
        if os.path.isfile(path_to_csv):
            print "PROBLEM ID " + problem_id
            problem_df = pandas.read_csv(path_to_csv)
            df = pandas.merge(contest_dict, problem_df, on = 'user_id')
            df = df[['user_id','rank','language']]
            list_of_frames.append(df)

        # merge tables for all problemes into one
        dframe = list_of_frames[0]
        groups = dframe.groupby('language')

        colors = ['b', 'c', 'y', 'm', 'r']
        var_index = 0
        color_pointer = 0
        f, ax = plt.subplots()
        for language,group in groups:
            list_of_users = group.user_id.tolist()
            l_of_users = range(var_index,var_index + len(list_of_users))
            l_of_rank = group['rank'].tolist()
            ax.scatter(l_of_users,l_of_rank,color= colors[color_pointer],label = language)
            color_pointer = color_pointer + 1
            var_index = var_index + len(l_of_users)

        plt.title("Contest " + contest_id)
        plt.ylabel("rank")
        plt.xlabel("user")
        plt.legend()
        plt.show()
        df = dframe[['rank','language']]
        print df
        df.boxplot(by='language')
        plt.title("Contest boxplot " + contest_id )
        plt.suptitle("")
        plt.show()

<<<<<<< HEAD
plot_rank_language()
=======
def test_pandas():
    cid_frame = pandas.read_csv(os.path.join(get_HOME_PATH(),'GCJ-backup','cid_pid_map_new.csv'))
    print cid_frame


def plot_cloc():
    for p_id in get_PROBLEM_IDS(gcj_path):
        for x in range(0,1):
            path_to_cloc = os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',p_id+'.csv'))
            x = []
            y = []
            languages = get_LANGUAGE()
            with open(path_to_cloc,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter=',')
                next(plots, None)  # skip the headers
                for row in plots:
                    if len(row)>0 :
                        x.append(int(row[4]))
                        y.append(languages.index(row[3]))
                    plt.yticks(range(len(languages)),languages)
                    plt.scatter(x,y, label='Cloc ' + p_id)
                    plt.xlabel('cloc')
                    plt.ylabel('Language')
                    plt.title('Interesting Graph\nCheck it out!')
                    plt.legend()
                    plt.show()

test_pandas()
>>>>>>> missingMainC++

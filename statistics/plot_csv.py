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



def create_one_frame() :
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    #create frame for contest csv
    list_of_frames = []
    for contest_id in get_CONTEST_IDS():
        print "CONTEST ID " + contest_id
        contest_dict = pandas.read_csv(os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',contest_id+'.csv')))
        problem_id_list = dict_cid_to_pid[contest_id]

        # create first frame by merging contest_csv with problem 0 input 0
        problem_zero = problem_id_list[0]
        path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(),problem_zero + '_0' +'.csv'))
        problem_df = pandas.read_csv(path_to_csv)
        df = pandas.merge(contest_dict, problem_df, on = 'user_id')
        df = df[['user_id','rank','language']]

        #merge first frame with problem 0 with input 1
        path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(),problem_zero + '_1' +'.csv'))
        if os.path.isfile(path_to_csv):
            problem_df = pandas.read_csv(path_to_csv)
            problem_df = problem_df [['user_id','language']]
            df = pandas.merge(df,problem_df, on = 'user_id',how='left')


        #merge with the rest
        for problem in problem_id_list[1:]:
            for x in ['0','1']:
                path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(),problem +'_'+ x +'.csv'))
                if os.path.isfile(path_to_csv):
                    problem_df = pandas.read_csv(path_to_csv)
                    problem_df = problem_df [['user_id','language']]
                    df = pandas.merge(df,problem_df, on = 'user_id',how = 'left')

        #filter contestats that have not used the same language:
        list_of_same_lang = []
        list_of_diff_lang = []
        for ind,row in df.iterrows():
            row = row.fillna('')
            row_list = row.iloc[2:].tolist()
            #if not all((x==row_list[0] or x =='')for x in row_list):
            #    df.drop(df.index[ind])
            if not all((x==row_list[0] or x =='') for x in row_list):
                list_of_same_lang.append(ind)
            else:
                list_of_diff_lang.append(ind)

        df = df.drop(df.index[list_of_same_lang])
        df1 = df.ix[:,1:3]

        list_of_frames.append(df1.groupby(['language_x'], as_index=False).mean())

    box = pandas.concat(list_of_frames).boxplot(by='language_x')
        #box = df1.boxplot(by='language_x')
    plt.ylabel("rank")
    plt.xlabel("language")
    plt.title("Boxplot Rank vs Language For All Competitions" )
    plt.suptitle("")

    fig = box.get_figure()
    fig_path = os.path.join(get_HOME_PATH(),'GCJ-backup','boxplot_rank_lang'+ '_rank_language_plot.png')

    fig.savefig(fig_path)

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



create_one_frame()


import pandas
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *


def init_dict() :
    return {'java': 0.0, 'Python': 0.0, 'C': 0.0, 'C++': 0.0, 'C#': 0.0}

def print_list(list_order) :
    res = ''
    for l in list_order :
        res += str(l) + ' < '
    return res[:len(res)-3]

def sort_langs(avg_dict) :
    sorted_means = sorted(avg_dict.keys())
    lang_order = []
    for sm in sorted_means :
        lang_order.append(avg_dict[sm])
    return lang_order, sorted_means

# gives a list of the languages
# with language with lowest avg
# rank first.
def order_langs_in_cid(c_id, cid_dict) :
    contest_dict = pandas.read_csv(os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',c_id+'.csv')))
    # get p_ids in this contest id
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    problem_ids = dict_cid_to_pid[c_id]
    IDS = get_PROBLEM_IDS_CONTEST(problem_ids)
    text = ''

    avg_total_dict = init_dict()
    complete_dict = {}
    for p_id in IDS :
        path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(), p_id +'.csv'))
        problem_df = pandas.read_csv(path_to_csv)
        df = pandas.merge(contest_dict, problem_df, on = 'user_id')
        df = df[['user_id', 'rank','language']]
        #df = df[np.isfinite(df['rank'])]
        avg_dict = {}
        avg_l_dict = init_dict()
        complete_dict[p_id] = avg_l_dict
        groups = df.groupby('language')
        for l,g in groups :
            if l != '-' :
                mean = g['rank'].mean()
                avg_dict[mean] = l
                avg_l_dict[l] = mean
                avg_total_dict[l] = avg_total_dict[l] + mean
   
        # sort langages
        lang_order, sorted_means = sort_langs(avg_dict)
        text += 'PROBLEM ID: ' + p_id + '\n'
        text += print_list(lang_order) + '\n'
        text += print_list(sorted_means) + '\n\n'
     
    # Do total mean 
    cid_dict[c_id] = avg_total_dict

    # write table to file
    path = os.path.join('../..', 'GCJ-backup', 'Tables', 'lang_order_' + c_id + '.txt')
    with open(path, 'wb') as file:
        file.write(text)
    print 'Done! wrote avg values and lang order to file in GCJ-backup/Tables'

    # Do some plots
    # x axis is problem ids
    
    x = range(0,len(IDS))
    y =  [None]*5 
    for idx, i in enumerate(y) :
        y[idx] = []

    for p_id in IDS :
        prob_dict = complete_dict[p_id]
        for idx, l in enumerate(prob_dict.keys()) :
            y[idx].append(prob_dict[l])

    language = complete_dict[IDS[0]].keys()
    colors = ['b', 'c', 'y', 'm', 'r']
    fig, ax = plt.subplots()
    for idx, lang_list in enumerate(y):
        ax.plot(x,lang_list,color= colors[idx],label = language[idx])
    plt.title("Contest " + c_id)
    plt.ylabel("Mean rank")
    plt.xlabel("Problem ID")
    plt.xticks(range(len(IDS)), IDS, rotation='vertical')
    plt.legend()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'mean_rank_' + c_id + '.png'))
    plt.close(fig)
    #plt.show()


def mean_plot_all(cid_dict, cids):
    languages = cid_dict[cids[0]].keys()

    x = range(0,len(cids))
    y =  [None]*5 
    for idx, i in enumerate(y) :
        y[idx] = []

    for c_id in cids :
        dict = cid_dict[c_id]
        for idx, l in enumerate(languages) :
            y[idx].append(dict[l]/5)
    colors = ['b', 'c', 'y', 'm', 'r']
    fig, ax = plt.subplots()
    for idx, lang_list in enumerate(y):
        ax.plot(x,lang_list,color= colors[idx],label = languages[idx])
    plt.title("Mean Rank" )
    plt.ylabel("Mean rank")
    plt.xlabel("Contest ID")
    plt.xticks(range(len(cids)), cids, rotation='vertical')
    plt.legend()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'mean_rank_all.png'))
    plt.close(fig)

 

def all_mean() :
    CONTEST_IDS = read_csv_file_to_dict('cid_pid_map_new.csv').keys()
    cid_dict = {}
    for c_id  in CONTEST_IDS :
        cid_dict[c_id] = {}
        order_langs_in_cid(c_id, cid_dict)
    # do some plot for all means / contest
    mean_plot_all(cid_dict, CONTEST_IDS)



all_mean()


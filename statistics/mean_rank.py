
import pandas
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import itertools 
from stats_help import *

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *


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

def plot_one_contest(c_id, IDS, complete_dict):
    # x axis is problem ids
    x = range(0,len(IDS))
    languages = complete_dict[IDS[0]].keys()
    # create one list of means for each language, 
    # list will contain mean for each pid
    y =  [None]*5 
    for idx, i in enumerate(y) :
        y[idx] = []

    # print names of pids
    x_labels = []
    for p_id in IDS :
        name = get_name_of_pid(p_id)
        letter = get_letter_of_pid(p_id)
        x_labels.append(letter)
        prob_dict = complete_dict[p_id]
        for idx, l in enumerate(languages) :
            y[idx].append(prob_dict[l])

    
    colors = get_COLORS()
    fig, ax = plt.subplots()
    for idx, lang_list in enumerate(y):
        ax.scatter(x,lang_list,color= colors[idx],label = languages[idx])
    plt.title("Contest " + c_id)
    plt.ylabel("Mean rank")
    plt.xlabel("Problem ID")
    plt.xticks(range(len(IDS)), x_labels, rotation='vertical')
    plt.legend()
    plt.tight_layout(w_pad=0.5, h_pad=1.8)
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures','mean_rank', 'mean_rank_' + c_id + '.png'))
    plt.close(fig)


# gives a list of the languages
# with language with lowest avg
# rank first.
def order_langs_in_cid(c_id, cid_dict) :
    print 'CONTEST: ' + c_id
    contest_dict = pandas.read_csv(os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',c_id+'.csv')))
    # get p_ids in this contest id
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    problem_ids = dict_cid_to_pid[c_id]
    IDS = get_PROBLEM_IDS_CONTEST(problem_ids)
    text = ''

    avg_total_dict = init_dict()
    complete_dict = {}
    csv_dict = {}
    print 'Number of problems: ' + str(len(IDS))
    print IDS
    for p_id in IDS :
        path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(), p_id +'.csv'))
        problem_df = pandas.read_csv(path_to_csv)
        df = pandas.merge(contest_dict, problem_df, on = 'user_id')
        print df
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

        # store to csv
        p_id_csv_dict = {}
        for idx,l in enumerate(lang_order):
            p_id_csv_dict['Rank_'+str(idx+1)] = l
            p_id_csv_dict['Value_'+str(idx+1)] = sorted_means[idx]
        csv_dict[p_id] = p_id_csv_dict

    
     
    # Do total mean 
    cid_dict[c_id] = avg_total_dict

    # write to csv
    path = os.path.join('../..', 'GCJ-backup', 'Tables', 'lang_order_' + c_id + '.csv')
    df = pandas.DataFrame.from_dict(csv_dict, orient='index')
    df.index.name = 'problem_id'
    df.to_csv(path)

    # plot one contest
    plot_one_contest(c_id, IDS, complete_dict)
    


# plots avg mean for contests as whole (total of p_ids in contest)
# creates graph of all contests
def mean_plot_all(cid_dict, cids):
    languages = cid_dict[cids[0]].keys()

    x = range(0,len(cids))
    y =  [None]*5 
    for idx, i in enumerate(y) :
        y[idx] = []

    # Calculate mean of all whole contest
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    for c_id in cids :
        dict = cid_dict[c_id]
        problem_ids = dict_cid_to_pid[c_id]
        IDS = get_PROBLEM_IDS_CONTEST(problem_ids)
        for idx, l in enumerate(languages) :
            y[idx].append(dict[l]/len(IDS))
    
    # print name of contest instead of ids
    cid_name_dict = get_cid_name_dict('c_id')
    x_label = []
    for cid in cids :
        name_dict = cid_name_dict[int(cid)] 
        x_label.append(name_dict['name'])

    colors = get_COLORS()
    fig, ax = plt.subplots()
    
    for idx, lang_list in enumerate(y):
        print idx
        print x
        print lang_list
        ax.plot(x,lang_list,color= colors[idx],label = languages[idx])
    plt.title("Mean Rank" )
    plt.ylabel("Mean rank")
    plt.xlabel("Contest")
    plt.xticks(range(len(cids)), x_label, rotation='vertical')
    plt.legend()
    plt.tight_layout(w_pad=0.5, h_pad=1.8)
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures','mean_rank', 'mean_rank_all.png'))
    plt.close(fig)

 
# wrrites to csv the toal avg mean rank in each contest
def all_mean() :
    CONTEST_IDS = get_CONTEST_IDS()
    cid_dict = {}
    csv_dict = {}
    for c_id  in CONTEST_IDS :
        cid_dict[c_id] = {}
        order_langs_in_cid(c_id, cid_dict)

        # dict to stor to csv
        csv_cid_dict = {}
        inv_dict = {v: k for k, v in cid_dict[c_id].iteritems()}
        lang_order, sorted_means = sort_langs(inv_dict)
        for idx,l in enumerate(lang_order):
            csv_cid_dict['Rank_'+str(idx+1)] = l
            csv_cid_dict['Value_'+str(idx+1)] = sorted_means[idx]
        csv_dict[c_id] = csv_cid_dict
    # stor total avg of mean rank in csv file
    path = os.path.join('../..', 'GCJ-backup', 'Tables', 'Total_lang_order_all_contests'  + '.csv')
    df = pandas.DataFrame.from_dict(csv_dict, orient='index')
    df.index.name = 'contest_id'
    df.to_csv(path)

    # do some plot for all means / contest
    mean_plot_all(cid_dict, CONTEST_IDS)

# Testede with
# A2 = 'ABCDEFGHIJKL'
# B2 = 'ABDCFEHGJILK'
# print kendall_tau(list(A2), list(B2))
# should be 0.85
def kendall_tau(A, B):
    # create two list with indexes of the ordering
    indexes_A = []
    index_lang_dict = {}
    for idx,a in enumerate(A) :
        index_lang_dict[a] = idx+1
        indexes_A.append(idx+1)
    indexes_B = []
    for b in B:
        indexes_B.append(index_lang_dict[b])
    dis = []
    con = []
    for idx,a in enumerate(indexes_A):
        b = indexes_B[idx]
        if a == b :
            con.append(len(indexes_A)-b)
            dis.append(0)
        elif a < b :
            con.append(len(indexes_A)-b)
            dis.append(1) 
        else :
            # a > b, copy previous con value
            con.append(con[idx-1])
            dis.append(0)
    c = float(sum(con))
    d = float(sum(dis))
    return (c - d) / (c + d)

# TODO change to matirx
def kendall_tau_matrix() :
    cids = get_CONTEST_IDS()
    text = ""
    path = os.path.join('../..', 'GCJ-backup', 'Tables', 'Total_lang_order_all_contests'  + '.csv')
    df = pandas.read_csv(path)
    rank_lists = [None]*len(cids)
    res = [None]*len(cids)
    for idx, c_id in enumerate(cids) :
        rank_lists[idx] = []
        res[idx] = [None]*len(cids)
        # read ordering
        for i in range(1,6) :
            lang = df.iloc[idx]['Rank_'+str(i)]
            rank_lists[idx] += [lang]

    for i, row1 in enumerate(rank_lists) :
        for j, row2 in enumerate(rank_lists) :    
            # compare list with next list
            diff_value = kendall_tau(row1, row2)
            res[i][j] = str("{0:.2f}".format(diff_value))
    return res
            
def print_kendall_tau_matrix(res) :
    header = 'Contest Name'
    contest_names = CIDS_name_timeline_order()
    for name in contest_names :
        header += ' & ' + '{\\tiny{\\rotatebox[origin=c]{90}{' + name + '}}}'
    header += '\\\\'
    print header
    # to fit on one page need to add {\small row_value}
    for idx, row in enumerate(res) :
        row = '{\\tiny ' + contest_names[idx] + '}' + ' & ' + ' & '.join(row) + '\\\\'
        print row
    #print C_ID_TIMELINE[idx+1] + ' & ' + print_list(rank_lists[idx+1]) + ' & ' + str("{0:.2f}".format(diff_value)) + '\\\\'
#create_cid_name_map()
#create_pid_name_map()
all_mean()
#res = kendall_tau_matrix()
#print_kendall_tau_matrix(res)






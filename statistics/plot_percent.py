
import pandas
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *

def init_dict() :
    return {'java': 0, 'Python': 0, 'C': 0, 'C++': 0, 'C#': 0}

def percent_compiled_competition(c_id) :
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    problem_ids = dict_cid_to_pid[c_id]
    # dictionaries contianing total values for all pid in cid
    # categorized by language
    nbr_copiled = init_dict()
    nbr_total = init_dict()
    for p_id  in get_PROBLEM_IDS_CONTEST(problem_ids) :
        for l in get_LANGUAGE() :
            path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(),p_id + '.csv'))
            df = pandas.read_csv(path_to_csv)
            try :
                # do pandas to get numbers
                # update some dict with all
                df = df[['language', 'compiled']]
                # df contains all rows with language l
                df = df.loc[df['language'] == l]
                nbr_total[l] = nbr_total[l] + df['language'].count()

                # df cotains all rows with compiled == 0 for language l
                df = df.loc[df['compiled'] == 0]
                nbr_copiled[l] = nbr_copiled[l] + df['compiled'].count()
            except :
                print 'File: ' + p_id + ' is not compiled!'
            
            print str(nbr_copiled[l]) + '/' + str(nbr_total[l]) + ' programs compiled succesfylly  in ' + l
    return nbr_copiled, nbr_total

def plot_bar_diagram(c_ids) :
    percents_total = []
    for c_id in c_ids :
        percents_cid = []
        # calculate percentage for one c_id
        compile_dict, total_dict = percent_compiled_competition(c_id)
        for l in total_dict.keys() :
        	try :
        		percent = float(compile_dict[l])/total_dict[l]
        	except :
        		percent = 0
        	percents_cid.append(percent)
        percents_total.append(percents_cid)
    #plot bar diagram    
    df2 = pandas.DataFrame(percents_total, columns=total_dict.keys(), index=c_ids)
    df2.plot.bar()
    plt.title("Percentage of successful compilation" )
    plt.ylabel("Percent")
    plt.xlabel("Contest")
    plt.show()



CONTEST_IDS = dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv').keys()
plot_bar_diagram(CONTEST_IDS)



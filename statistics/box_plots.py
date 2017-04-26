import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas as pd
from stats_help import *

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *

# box plot for trait in column problem by problem
def general_box_plot_problem(p_id, y_label, column) :
    print p_id
    path = os.path.join('../..', 'GCJ-backup', p_id+'.csv')
    df = pd.read_csv(path)
    try:
        data = df[['language', column]].astype(str)
        data = data.loc[data[column] != '-']
        data = data.apply(pd.to_numeric, errors='ignore')
        try:
            box = data.boxplot(by='language', showfliers=False)
            plt.title(y_label +', '+ get_name_of_pid(p_id))
            plt.ylabel(y_label)
            plt.xlabel("Language")
            plt.suptitle('')
            #plt.show()
            fig = box.get_figure()
            fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', column, 'box_plot_'+column+'_'+p_id+'.png'))
        except ValueError:
            print 'skiped: ' + p_id
            print 'problem not compiled yet'
    except KeyError:
        print 'skiped: ' + p_id
        print 'column does not exist'

def all_problem_by_problem() :
    p_ids = get_PROBLEM_IDS(os.path.join('../'))
    columns = ['cloc', 'max_RAM', 'exe_size', 'wall_clock', 'user_time']
    ylabels = ['Lines of Code', 'Memory footprint (Bytes)', 'Size of Executable File', 'Wall Clock', 'User Time']
    for p_id in p_ids :
        for idx,c in enumerate(columns):
            print 'BOX PLOT FOR: ' + c
            general_box_plot_problem(p_id, ylabels[idx], c)



# total plot for all problems
def general_box_plot(column, save_to_filename, y_label, title) :

    data = get_all_data([column, 'language'])
    # all data is collected
    # remove all rows where value is -
    data = data.loc[data[column] != '-']
    # conver data to int
    data = data.apply(pd.to_numeric, errors='ignore')
    #do boxplot
    box = data.boxplot(by='language', showfliers=False)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel("Language")
    plt.suptitle('')
    #plt.show()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', save_to_filename))
  
## call to do plots for total
def do_all_total() :
    general_box_plot('cloc', 'box_plot_cloc_total.png', 'Lines of Code', 'Lines of Code, all competitions' )
    general_box_plot('exe_size', 'box_plot_exe_size_total.png', 'Size of Executable File', 'Size of Executable, all competitions')
    general_box_plot('max_RAM', 'box_plot_memory_total.png', 'Memory footprint (Bytes)', 'Memory footprint, all competitions')
    general_box_plot('wall_clock', 'box_plot_wall_cloc_total.png', 'Wall Clock', 'Wall Clocl, all competitions' )
    general_box_plot('user_time', 'box_plot_user_time_total.png', 'User Time', 'User Time, all competitions' )

#general_box_plot_problem('5648941810974720_0', 'max_RAM', 'max_RAM')


all_problem_by_problem()


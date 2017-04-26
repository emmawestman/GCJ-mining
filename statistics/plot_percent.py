
import pandas
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from stats_help import *

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *

def total_percent_plot() :
    languages = ['C', 'C#', 'C++', 'Java', 'Python']
    data = get_all_data(['language', 'compiled', 'exit_code'])
    # nbr total
    df = data.groupby('language')
    total = df.size()
    totals = []
    totals.append(total[0])
    totals.append(total[1])
    totals.append(total[2])
    totals.append(total[3])
    totals.append(total[4])
    
    # nbr runs
    df_run = data.loc[data['exit_code'] == 0]
    df = df_run.groupby('language')
    run = df.size()
    runs = []
    runs.append(float(run[0])/total[0])
    runs.append(float(run[1])/total[1])
    runs.append(float(run[2])/total[2])
    runs.append(float(run[3])/total[3])
    runs.append(float(run[4])/total[4])

    # nbr compiles
    df_comp = data.loc[data['compiled'] == 0]
    df = df_comp.groupby('language')
    comp = df.size()
    comps = []
    comps.append(float(comp[0]-run[0])/total[0])
    comps.append(float(comp[1]-run[1])/total[1])
    comps.append(float(comp[2]-run[2])/total[2])
    comps.append(float(comp[3]-run[3])/total[3])
    comps.append(float(comp[4]-run[4])/total[4])

    # nbr rest
    rests = []
    rests.append(1 - runs[0] -comps[0])
    rests.append(1 - runs[1] -comps[1])
    rests.append(1 - runs[2] -comps[2])
    rests.append(1 - runs[3] -comps[3])
    rests.append(1 - runs[4] -comps[4])

    print runs
    print comps
    print rests

    df2 = pd.DataFrame()
    df2['language'] = languages
    df2['executed'] = runs
    df2['comiled'] = comps
    df2['total'] = rests
    

    df2.plot.bar(stacked=True, color=['#2255a5', '#5e8cd6', '#9dbae8'])
    plt.ylabel("Percentage")
    plt.xlabel("language")
    plt.xticks(range(len(languages)), languages)
    plt.show()


def init_dict() :
    return {'Java': 0, 'Python': 0, 'C': 0, 'C++': 0, 'C#': 0}

# percent of  [exit_code==0]/[compiled==0]
def percent_column2(c_id, column1, column2) :
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    problem_ids = dict_cid_to_pid[c_id]
    # dictionaries contianing total values for all pid in cid
    # categorized by language
    nbr_column = init_dict()
    nbr_total = init_dict()
    for p_id  in get_PROBLEM_IDS_CONTEST(problem_ids) :
        for l in get_LANGUAGE() :
            path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(),p_id + '.csv'))
            df = pandas.read_csv(path_to_csv)
            try :
                # do pandas to get numbers
                # update some dict with all
                df = df[['language', column1, column2]]
                # df contains all rows with language l
                df = df.loc[df['language'] == l]
                df = df.loc[df[column2] == 0]
                nbr_total[l] = nbr_total[l] + df[column2].count()

                # df cotains all rows with compiled == 0 for language l
                df = df.loc[df[column1] == 0]
                nbr_column[l] = nbr_column[l] + df[column1].count()
            except :
                print 'File: ' + p_id + ' is not compiled!'
            
            print str(nbr_column[l]) + '/' + str(nbr_total[l]) + ' programs ran/succesfylly compiled  in ' + l
    return nbr_column, nbr_total

# percent ofc column [v==0]/column
def percent_column(c_id, column) :
    dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv')
    problem_ids = dict_cid_to_pid[c_id]
    # dictionaries contianing total values for all pid in cid
    # categorized by language
    nbr_column = init_dict()
    nbr_total = init_dict()
    for p_id  in get_PROBLEM_IDS_CONTEST(problem_ids) :
        for l in get_LANGUAGE() :
            path_to_csv = os.path.realpath(os.path.join(get_GCJ_BACKUP_PATH(),p_id + '.csv'))
            df = pandas.read_csv(path_to_csv)
            try :
                # do pandas to get numbers
                # update some dict with all
                df = df[['language', column]]
                # df contains all rows with language l
                df = df.loc[df['language'] == l]
                nbr_total[l] = nbr_total[l] + df[column].count()

                # df cotains all rows with compiled == 0 for language l
                df = df.loc[df[column] == 0]
                nbr_column[l] = nbr_column[l] + df[column].count()
            except :
                print 'File: ' + p_id + ' is not compiled!'
            
            print str(nbr_column[l]) + '/' + str(nbr_total[l]) + ' programs compiled succesfylly  in ' + l
    return nbr_column, nbr_total

# compiled/all
def percent_compiled(c_id) :
	return percent_column(c_id, 'compiled')

# run/all
def percent_run_all(c_id) :
	return percent_column(c_id, 'exit_code')

# run/compiled
def percent_run_compile(c_id):
	return percent_column2(c_id, 'exit_code', 'compiled')


def plot_bar_diagram_compile(c_ids) :
    percents_total = []
    for c_id in c_ids :
        percents_cid = []
        # calculate percentage for one c_id
        compile_dict, total_dict = percent_compiled(c_id)
        for l in total_dict.keys() :
        	try :
        		percent = float(compile_dict[l])/total_dict[l]
        	except :
        		percent = 0
        	percents_cid.append(percent)
        percents_total.append(percents_cid)
    #plot bar diagram    
    df2 = pandas.DataFrame(percents_total, columns=total_dict.keys(), index=c_ids)
    bar = df2.plot.bar(color=get_COLORS())
    plt.title("Percentage of successful compilation" )
    plt.ylabel("Percent")
    plt.xlabel("Contest")
    plt.show()
    return bar.get_figure()

def plot_bar_diagram_run(c_ids) :
    percents_total = []
    for c_id in c_ids :
        percents_cid = []
        # calculate percentage for one c_id
        run_dict, total_dict = percent_run_all(c_id)
        for l in total_dict.keys() :
        	try :
        		percent = float(run_dict[l])/total_dict[l]
        	except :
        		percent = 0
        	percents_cid.append(percent)
        percents_total.append(percents_cid)
    #plot bar diagram    
    df2 = pandas.DataFrame(percents_total, columns=total_dict.keys(), index=c_ids)
    bar = df2.plot.bar(color=get_COLORS())
    plt.title("Percentage of successful runs" )
    plt.ylabel("Percent")
    plt.xlabel("Contest")
    plt.show()
    return bar.get_figure()

def plot_bar_diagram_run_comp(c_ids) :
    percents_total = []
    for c_id in c_ids :
        percents_cid = []
        # calculate percentage for one c_id
        run_dict, total_dict = percent_run_compile(c_id)
        for l in total_dict.keys() :
        	try :
        		percent = float(run_dict[l])/total_dict[l]
        	except :
        		percent = 0
        	percents_cid.append(percent)
        percents_total.append(percents_cid)
    #plot bar diagram    
    df2 = pandas.DataFrame(percents_total, columns=total_dict.keys(), index=c_ids)
    bar = df2.plot.bar(color=get_COLORS())
    plt.title("Percentage of successful runs/compilation" )
    plt.ylabel("Percent")
    plt.xlabel("Contest")
    plt.show()
    return bar.get_figure()


total_percent_plot() 



CONTEST_IDS = dict_cid_to_pid = read_csv_file_to_dict('cid_pid_map_new.csv').keys()
fig1 = plot_bar_diagram_compile(CONTEST_IDS)
fig1.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'compiled_percent.png'))

fig2 = plot_bar_diagram_run(CONTEST_IDS)
fig2.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'run_percent.png'))

fig3  = plot_bar_diagram_run_comp(CONTEST_IDS)
fig3.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'run_compiled_percent.png'))




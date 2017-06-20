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
        # only for cloc
        #data = data.loc[data[column] != '0']
        data = data.apply(pd.to_numeric, errors='ignore')
        try:
            box = data.boxplot(by='language', showfliers=False)
            counts = data.groupby('language').count()
            if len(counts) == 5 :
                nbrC = counts.iloc[0][column]
                nbrCsharp = counts.iloc[1][column]
                nbrCplus = counts.iloc[2][column]
                nbrJava = counts.iloc[3][column]
                nbrPython = counts.iloc[4][column]
                x_labels = ['C, '+str(nbrC), 'C#, '+str(nbrCsharp), 'C++, '+str(nbrCplus), 'Java, '+str(nbrJava), 'Python, '+str(nbrPython)]
                box.set_xticklabels(x_labels, rotation=0)
            else :
                print 'fix the x lables maybe'
            plt.xlabel("Language, Number of Files")
            plt.title(y_label +', '+ get_name_of_pid(p_id))
            plt.ylabel(y_label)
            plt.suptitle('')
            #plt.show()
            plt.tight_layout()
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

def sys_user_time_plot(save_to_filename, y_label, title) :
    data = get_all_data(['user_time', 'system_time', 'language'])
    data = data.loc[data['system_time'] != '-']
    data = data.apply(pd.to_numeric, errors='ignore')
    tot_time_df = pd.DataFrame()
    tot_time_df['language'] = data['language']
    tot_time_df['tot_time'] = data['system_time'] + data['user_time']

    box = tot_time_df.boxplot(by='language', showfliers=False)
    counts = tot_time_df.groupby('language').count()

    nbrC = counts.iloc[0]['tot_time']
    nbrCsharp = counts.iloc[1]['tot_time']
    nbrCplus = counts.iloc[2]['tot_time']
    nbrJava = counts.iloc[3]['tot_time']
    nbrPython = counts.iloc[4]['tot_time']
    plt.ylabel(y_label)
    x_labels = ['C, '+str(nbrC), 'C#, '+str(nbrCsharp), 'C++, '+str(nbrCplus), 'Java, '+str(nbrJava), 'Python, '+str(nbrPython)]
    box.set_xticklabels(x_labels, rotation=0)
    plt.xlabel("Language, Number of Files")
    plt.title(title)
    plt.suptitle('')
    #plt.show()
    plt.tight_layout()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', save_to_filename))


# total plot for all problems
def general_box_plot(column, save_to_filename, y_label, title) :
    data = get_all_data([column, 'language'])
    # all data is collected
    # remove all rows where value is -
    data = data.loc[data[column] != '-']
    # conver data to int
    data = data.apply(pd.to_numeric, errors='ignore')
    #do
    counts = data.groupby('language').count()
    print counts
    box = data.boxplot(by='language', showfliers=False)
    counts = data.groupby('language').count()

    nbrC = counts.iloc[0][column]
    nbrCsharp = counts.iloc[1][column]
    nbrCplus = counts.iloc[2][column]
    nbrJava = counts.iloc[3][column]
    nbrPython = counts.iloc[4][column]
    plt.ylabel(y_label)
    x_labels = ['C, '+str(nbrC), 'C#, '+str(nbrCsharp), 'C++, '+str(nbrCplus), 'Java, '+str(nbrJava), 'Python, '+str(nbrPython)]
    box.set_xticklabels(x_labels, rotation=0)
    plt.xlabel("Language, Number of Files")
    plt.title(title)
    plt.suptitle('')
    #plt.show()
    plt.tight_layout()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', save_to_filename))


def get_data_frame(col):
    column = 'cloc'
    data = get_all_data(['language','exit_code','cloc',col])
    # conver data to int
    data = data.apply(pd.to_numeric, errors='ignore')
    data = data.loc[data['exit_code']== 0]
    df_java = data.loc[data['language'] == 'Java']

    df_csharp = data.loc[data['language'] == 'C#']
    df_cplus =  data.loc[data['language'] == 'C++']
    df_python = data.loc[data['language'] == 'Python']
    df_c = data.loc[data['language'] == 'C']

    df_java = df_java.loc[df_java[column]>15]
    df_c = df_c.loc[df_c[column]>10]
    df_cplus = df_cplus.loc[df_cplus[column]>10]
    df_csharp = df_csharp.loc[df_csharp[column]>15]
    df_python = df_python.loc[df_python[column]>0]

    frames = [df_java,df_python,df_c,df_csharp,df_cplus]
    data = pd.concat(frames)
    return pd.DataFrame(data[['language',col]].as_matrix(), columns=['language',col])

def plot_box(column,data,output,y_label,title):
    box = data.boxplot(by='language',sym='')

    counts = data.groupby('language').count()

    nbrC = counts.iloc[0][column]
    nbrCsharp = counts.iloc[1][column]
    nbrCplus = counts.iloc[2][column]
    nbrJava = counts.iloc[3][column]
    nbrPython = counts.iloc[4][column]
    plt.ylabel(y_label)
    x_labels = ['C, '+str(nbrC), 'C#, '+str(nbrCsharp), 'C++, '+str(nbrCplus), 'Java, '+str(nbrJava), 'Python, '+str(nbrPython)]
    box.set_xticklabels(x_labels, rotation=0)
    plt.xlabel("Language, Number of Files")
    plt.title(title)
    plt.suptitle('')
    #plt.show()
    plt.tight_layout()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', output))




def verified_box_plot_cloc():
    data = get_data_frame(col='cloc')
    plot_box('cloc',data,output='box_plot_cloc_total.png', y_label = 'Lines of Code', title = 'Lines of Code, all competitions' )

def verified_box_plot_exe():
    data = get_data_frame(col='exe_size')
    plot_box('exe_size',data,output='box_plot_exe_size_total.png', y_label='Size of Executable File', title='Size of Executable, all competitions')

def verified_box_plot_ram():
    data = get_data_frame(col='max_RAM')
    plot_box('max_RAM',data,output='box_plot_memory_total.png', y_label= 'Memory footprint (Bytes)', title='Memory footprint, all competitions')

def verified_box_plot_wall_cloc():
    data = get_data_frame(col='wall_clock')
    plot_box('wall_clock',data,output='box_plot_wall_cloc_total.png', y_label='Wall Clock (s)', title='Wall Clock, all competitions')

def verified_box_plot_user():
    data=get_data_frame(col='user_time')
    plot_box('user_time',data,output='box_plot_user_time_total.png', y_label='User Time (s)', title='User Time, all competitions')

## call to do plots for total
def do_all_total() :
    general_box_plot('cloc', 'box_plot_cloc_total.png', 'Lines of Code', 'Lines of Code, all competitions' )
    general_box_plot('exe_size', 'box_plot_exe_size_total.png', 'Size of Executable File', 'Size of Executable, all competitions')
    general_box_plot('max_RAM', 'box_plot_memory_total.png', 'Memory footprint (Bytes)', 'Memory footprint, all competitions')
    general_box_plot('wall_clock', 'box_plot_wall_cloc_total.png', 'Wall Clock (s)', 'Wall Clock, all competitions' )
    general_box_plot('user_time', 'box_plot_user_time_total.png', 'User Time (s)', 'User Time, all competitions' )
    #sys_user_time_plot('box_plot_tot_time_total.png', 'User + System Time (s)', 'User + System Time, all competitions')

#general_box_plot_problem('5648941810974720_0', 'max_RAM', 'max_RAM')
verified_box_plot_exe()

#all_problem_by_problem()

def clean_csv() :
    pids = get_PROBLEM_IDS(gcj_path)
    path = os.path.join(os.getcwd(), '..','..', 'GCJ-backup')
    for pid in pids :
        print pid
        filename = os.path.join(path, pid+'.csv')
        dict = read_csv_file(filename)
        contestants = dict.keys()
        for c in contestants :
            c_dict = dict[c]
            if c_dict['language'] == 'C#':
                if '\"' in c_dict['compile_error_msg'] :
                    print 'updating :' + pid
                    oldstr = c_dict['compile_error_msg']
                    newstr = oldstr.replace(":", "")
                    newstr = oldstr.replace("\"", "")
                    c_dict['compile_error_msg'] = newstr
                    c_dict['run_error_msg'] = '-'
                    c_dict['max_RAM'] = '-'
                    c_dict['user_time'] = '-'
        write_to_csv_file(filename, dict)

def clean_csv2() :
    pids = get_PROBLEM_IDS(gcj_path)
    path = os.path.join(os.getcwd(), '..','..', 'GCJ-backup')
    for pid in pids :
        print pid
        filename = os.path.join(path, pid+'.csv')
        dict = read_csv_file(filename)
        contestants = dict.keys()
        for c in contestants :
            c_dict = dict[c]
            if c_dict['max_RAM'] != '-' and type(c_dict['max_RAM']) != int:
                try :
                    int(c_dict['max_RAM'])
                except ValueError:
                    c_dict['max_RAM'] = '-'
                    print c
                    print c_dict['max_RAM']
                    print type(c_dict['max_RAM'])
        write_to_csv_file(filename, dict)
#clean_csv2()
verified_box_plot_exe()

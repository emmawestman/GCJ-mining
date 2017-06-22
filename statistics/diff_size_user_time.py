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

# select all user_id, user_time where exit_code == 0 for both size 0 and 1
def diff_user_time():
    all_data = pd.DataFrame()
    p_ids = get_PROBLEM_IDS_BOTH(os.path.join('../'))
    for p_id in p_ids:
        print p_id
        path1 = os.path.join('../..', 'GCJ-backup', p_id+'_0.csv')
        path2 = os.path.join('../..', 'GCJ-backup', p_id+'_1.csv')
        df1 = pd.read_csv(path1)
        df2 = pd.read_csv(path2)
        try:
            df1 = df1[['user_id', 'language', 'user_time', 'exit_code']].astype(str)
            df1.rename(columns={'user_time' : 'user_time_0'},inplace=True)
            df1 = df1.loc[df1['exit_code'] == '0']

            df2 = df2[['user_id', 'language', 'user_time', 'exit_code']].astype(str)
            df2.rename(columns={'user_time' : 'user_time_1'},inplace=True)
            df2 = df2.loc[df2['exit_code'] == '0']

            data = df1.merge(df2, left_on='user_id', right_on='user_id', how='inner')
            data = data.loc[data['language_x'] == data['language_y']]
            data.rename(columns={'language_x' : 'language'},inplace=True)
            data = data[['user_id', 'language', 'user_time_0', 'user_time_1']]
            data['problem_id'] = p_id

            data = data.loc[data['user_time_1'] != '-']
            data = data.loc[data['user_time_0'] != '-']
            data1 = data['user_time_1'].apply(pd.to_numeric)
            data0 = data['user_time_0'].apply(pd.to_numeric)
            data['diff_user_time'] = data1 - data0

#            new_data = pd.DataFrame()
#            data1 = data['user_time_1']
#            data1 =data1.apply(pd.to_numeric, errors='ignore')
#            data0 = data['user_time_0']
#            data0 =data0.apply(pd.to_numeric, errors='ignore')
#            new_data['diff_user_time'] = data1[['user_time_1']]-data0[['user_time_0']]
#            new_data['language'] = data[['language']]
            df = data[['diff_user_time', 'language']]
            all_data = all_data.append(df)
            
        except KeyError:
            #df = df['language']
            #size = len(df.index)
            #for c in columns:
                #df[c] = ['-']*size
            print 'skiped: ' + p_id
    print all_data
    box = all_data.boxplot(by='language', showfliers=False)
    counts = all_data.groupby('language').count()
    column = 'diff_user_time'
    if len(counts) == 5 :
        nbrC = counts.iloc[0][column]
        nbrCsharp = counts.iloc[1][column]
        nbrCplus = counts.iloc[2][column]
        nbrJava = counts.iloc[3][column]
        nbrPython = counts.iloc[4][column]
        x_labels = ['C, '+str(nbrC), 'C#, '+str(nbrCsharp), 'C++, '+str(nbrCplus), 'Java, '+str(nbrJava), 'Python, '+str(nbrPython)]
        box.set_xticklabels(x_labels, rotation=0)
    plt.xlabel("Language, Number of Files")
    plt.title('Diff in user time small and large input')
    plt.ylabel('Time (s)')
    plt.suptitle('')
    plt.tight_layout()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'box_plot_diff_user_time_total.png'))


def diff_memory():
    all_data = pd.DataFrame()
    p_ids = get_PROBLEM_IDS_BOTH(os.path.join('../'))
    for p_id in p_ids:
        print p_id
        path1 = os.path.join('../..', 'GCJ-backup', p_id+'_0.csv')
        path2 = os.path.join('../..', 'GCJ-backup', p_id+'_1.csv')
        df1 = pd.read_csv(path1)
        df2 = pd.read_csv(path2)
        try:
            df1 = df1[['user_id', 'language', 'max_RAM', 'exit_code']].astype(str)
            df1.rename(columns={'max_RAM' : 'max_RAM_0'},inplace=True)
            df1 = df1.loc[df1['exit_code'] == '0']

            df2 = df2[['user_id', 'language', 'max_RAM', 'exit_code']].astype(str)
            df2.rename(columns={'max_RAM' : 'max_RAM_1'},inplace=True)
            df2 = df2.loc[df2['exit_code'] == '0']

            data = df1.merge(df2, left_on='user_id', right_on='user_id', how='inner')
            data = data.loc[data['language_x'] == data['language_y']]
            data.rename(columns={'language_x' : 'language'},inplace=True)
            data = data[['user_id', 'language', 'max_RAM_0', 'max_RAM_1']]
            data['problem_id'] = p_id

            data = data.loc[data['max_RAM_1'] != '-']
            data = data.loc[data['max_RAM_0'] != '-']
            data1 = data['max_RAM_1'].apply(pd.to_numeric)
            data0 = data['max_RAM_0'].apply(pd.to_numeric)
            data['diff_max_RAM'] = data1 - data0

#            new_data = pd.DataFrame()
#            data1 = data['user_time_1']
#            data1 =data1.apply(pd.to_numeric, errors='ignore')
#            data0 = data['user_time_0']
#            data0 =data0.apply(pd.to_numeric, errors='ignore')
#            new_data['diff_user_time'] = data1[['user_time_1']]-data0[['user_time_0']]
#            new_data['language'] = data[['language']]
            df = data[['diff_max_RAM', 'language']]
            all_data = all_data.append(df)
            
        except KeyError:
            #df = df['language']
            #size = len(df.index)
            #for c in columns:
                #df[c] = ['-']*size
            print 'skiped: ' + p_id
    print all_data
    box = all_data.boxplot(by='language', showfliers=False)
    counts = all_data.groupby('language').count()
    column = 'diff_max_RAM'
    if len(counts) == 5 :
        nbrC = counts.iloc[0][column]
        nbrCsharp = counts.iloc[1][column]
        nbrCplus = counts.iloc[2][column]
        nbrJava = counts.iloc[3][column]
        nbrPython = counts.iloc[4][column]
        x_labels = ['C, '+str(nbrC), 'C#, '+str(nbrCsharp), 'C++, '+str(nbrCplus), 'Java, '+str(nbrJava), 'Python, '+str(nbrPython)]
        box.set_xticklabels(x_labels, rotation=0)
    plt.xlabel("Language, Number of Files")
    plt.title('Diff in memory consumption small and large input')
    plt.ylabel('Time (s)')
    plt.suptitle('')
    plt.tight_layout()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'box_plot_diff_max_RAM_total.png'))


diff_memory()
diff_user_time()



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


# table for total number of solutions, soltions with LOC, compiled, executed
def print_table():
    columns =['language', 'user_id', 'cloc', 'compiled', 'exit_code']
    language = ['C', 'C#', 'C++', 'Java','Python']
    data = get_all_data(columns)

    frames = []
    df1 = data[['language', 'user_id']].astype(str)
    df1 = df1.loc[df1['user_id'] != '-']
    df1 = df1.groupby('language').count()
    print df1
    frames.append(df1)

    df2 = data[['language', 'cloc']].astype(str)
    df2 = df2.loc[df2['cloc'] != '-']
    df2 = df2.groupby('language').count()
    print df2
    frames.append(df2)

    df3 = data[['language', 'compiled']].astype(str)
    df3 = df3.loc[df3['compiled'] != '-']
    df3 = df3.loc[df3['compiled'] == '0']
    df3 = df3.groupby('language').count()
    print df3
    frames.append(df3)

    df4 = data[['language', 'exit_code']].astype(str)
    df4 = df4.loc[df4['exit_code'] != '-']
    df4 = df4.loc[df4['exit_code'] == '0']
    df4 = df4.groupby('language').count()
    print df4
    frames.append(df4)
    
    all_strings = []
    overall_values = [0, 0, 0, 0]
    for i,l in enumerate(language) :
        string = l 
        for j,c in enumerate(columns[1:]) :
            string = string +  ' & ' + str(frames[j].iloc[i][c])
            overall_values[j] = overall_values[j] + frames[j].iloc[i][c]
        string = string + '\\\\'
        all_strings.append(string)
  

    print '\\begin{table}[H]'
    print '\\centering'
    print '\\caption{Number of Solutions}'
    print '\\label{tab:nbr_of_sol}'
    print '\\begin{tabular}{ccccc}'
    print '\\toprule'
    print     'Language & Number of Solutions & LOC & Compiled & Executed \\\\'
    print     '\\midrule'
    print all_strings[0]
    print all_strings[1]
    print all_strings[2]
    print all_strings[3]
    print all_strings[4]
    print '    \\midrule'
    print '    Total & ' + str(overall_values[0]) + ' & ' + str(overall_values[1]) + ' & ' + str(overall_values[2]) + ' & ' + str(overall_values[3]) + '\\\\'
    print '\\bottomrule'
    print '\\end{tabular}'
    print '\\end{table}'

# zip neds to be checked out idatacollection
def number_downloaded_total() :
	problem_ids = get_PROBLEM_IDS(os.path.join('..'))
	number_of_sol = 0
	for prob_id in problem_ids :
		print prob_id
		path = os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection', 'solutions_' + prob_id))
		#print os.listdir(path)
		number_of_sol += len(os.listdir(path))
	print number_of_sol


#number_downloaded_total()
print_table()


















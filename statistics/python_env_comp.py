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

def total_python_percent_plot() :
    env = ['2.x', '3.x']
    data = get_all_data(['language', 'compiled', 'exit_code', 'compiler_version', 'user_id'])
    data = data.loc[data['language'] == 'Python']
    data = data.loc[data['compiler_version'] != '-']
    # nbr total
    df = data.groupby('compiler_version')
    
    total = df.size()
    print total
    totals = []
    totals.append(total[0])
    totals.append(total[1])
    
    # nbr runs
    df_run = data.loc[data['exit_code'] == 0]
    df = df_run.groupby('compiler_version')
    run = df.size()
    print run
    runs = []
    runs.append(float(run[0])/total[0])
    runs.append(float(run[1])/total[1])

    # nbr compiles
    df_comp = data.loc[data['compiled'] == 0]
    df = df_comp.groupby('compiler_version')
    comp = df.size()
    print comp
    comps = []
    comps.append(float(comp[0]-run[0])/total[0])
    comps.append(float(comp[1]-run[1])/total[1])

    # nbr rest
    rests = []
    rests.append(1 - runs[0] -comps[0])
    rests.append(1 - runs[1] -comps[1])

    print rests

    df2 = pd.DataFrame()
    df2['compiler_version'] = env
    df2['executed'] = runs
    df2['comiled'] = comps
    df2['total'] = rests
    
    print df2

    bar = df2.plot.bar(stacked=True, color=['#2255a5', '#5e8cd6', '#9dbae8'])
    plt.ylabel("Percentage")
    plt.xlabel("Python Environment")
    bar.set_xticklabels(env, rotation=0)
    #plt.show()
    plt.tight_layout()
    fig = bar.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'Python_total_percent_run_compile.png'))
    plt.clf()

# total plot for all problems
def version_distribution_plot() :

    data = get_all_data(['language', 'compiler_version', 'user_id'])
    # all data is collected
    # remove all rows where value is -
    data = data.loc[data['language'] == 'Python']
    data = data.loc[data['compiler_version'] != '-']
    #data = data.loc[data['compiler_version'] != '2.7']
    #print data.loc[data['compiler_version'] != '3.5']
    
    df = data.groupby('compiler_version')
    size = df.size()
    print size
    sizes = []
    sizes.append(size[0])
    sizes.append(size[1])
   
    df = pd.DataFrame()
    df['Env'] = ['2.x', '3.x']
    df['count'] = sizes
    print df

    
    bar = df['count'].plot(kind='bar', color=['#2255a5'], legend=False)
    bar.set_xticklabels(['2.x', '3.x'], rotation=0)
    
    bar.set_xlabel("Python Environment")
    bar.set_ylabel("Number of files")
    
    #pie = df['count'].plot.pie(colors=get_COLORS(),labels=df['Env'], autopct='%1.1f%%', textprops=dict(fontname="Tahoma", fontsize=12, weight='bold'))

    #plt.legend()
    plt.suptitle('')
    plt.title('Distribution of usage of Python Environments')
    plt.show()
    #plt.tight_layout()
    fig = bar.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'Python_distribution.png'))
    


def general_box_plot(column, save_to_filename, y_label, title):
    data = get_all_data([column, 'language', 'compiler_version'])
    # all data is collected
    # remove all rows where value is -
    data = data.loc[data['language'] == 'Python']
    data = data.loc[data['compiler_version'] != '-']
    data = data.loc[data[column] != '-']
    data = data.apply(pd.to_numeric, errors='ignore')
    #do boxplot
    box = data.boxplot(by='compiler_version', showfliers=False)
    counts = data.groupby('compiler_version').count()
    nbr2x = counts.iloc[0]['language']
    nbr3x = counts.iloc[1]['language']
    plt.title(title)
    plt.ylabel(y_label)
    x_labels = ['2.x, '+str(nbr2x), '3.x, '+str(nbr3x)]
    box.set_xticklabels(x_labels, rotation=0)
    plt.xlabel("Python Environment, Number of Files")
    plt.suptitle('')
    #plt.show()
    plt.tight_layout()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', save_to_filename))
  


def do_all_total() :
    general_box_plot('cloc', 'Python_box_plot_cloc_total.png', 'Python, Lines of Code', 'Lines of Code, all competitions' )
    general_box_plot('exe_size', 'Python_box_plot_exe_size_total.png', 'Python, Size of Executable File', 'Size of Executable, all competitions')
    general_box_plot('max_RAM', 'Python_box_plot_memory_total.png', 'Python, Memory footprint (Bytes)', 'Memory footprint, all competitions')
    general_box_plot('wall_clock', 'Python_box_plot_wall_cloc_total.png', 'Python, Wall Clock (s)', 'Wall Clock, all competitions' )
    general_box_plot('user_time', 'Python_box_plot_user_time_total.png', 'Python, User Time (s)', 'User Time, all competitions' )


#total_python_percent_plot()
version_distribution_plot()
#do_all_total()








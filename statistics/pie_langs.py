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


def distribution_langs() :
    data = get_all_data(['language'])
    total_nbr_of_files = data.count()[0] +1

  
    df = data.groupby('language')
    size = df.size()
    sizes = []
    sizes.append(size[0])
    sizes.append(size[1])
    sizes.append(size[2])
    sizes.append(size[3])
    sizes.append(size[4])
    
   
    df = pd.DataFrame()
    df['language'] = ['C', 'C#', 'C++', 'Java', 'Python']
    df['count'] = sizes

    bar = df.plot(kind='bar', color=['#2255a5'], legend=False)
    bar.set_xticklabels(['C', 'C#', 'C++', 'Java', 'Python'], rotation=0)
    
    bar.set_xlabel("Language")
    bar.set_ylabel("Number of files")

    #plt.legend()
    plt.suptitle('')
    plt.tight_layout()
    plt.show()
    fig = bar.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'lang_distribution.png'))

    ## print table of number of solutions in each language
    print '\\begin{table}[h!]'
    print '\\centering'
    print '\\caption{Number of Solutions}'
    print '\\label{tab:nbr_of_sol}'
    print '\\begin{tabular}{cc}'
    print '\\toprule'
    print '    Language & Number of solutions \\ \\\\'
    print '    \midrule'
    print '    C & '+  str(size[0]) +' \\\\'
    print '    C# & ' +  str(size[1]) +'\\\\'
    print '    C++ & ' + str(size[2]) +'\\\\'
    print '    Java  & ' + str(size[3]) +'\\\\'
    print '    Python & ' + str(size[4]) +'\\\\'
    print '    \midrule'
    print '    Total number of Solutions: & ' + str(total_nbr_of_files) +'\\\\'
    print '\\bottomrule'
    print '\\end{tabular}'
    print '\\end{table}'

distribution_langs() 










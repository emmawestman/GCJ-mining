import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas as pd
from stats_help import *


def distribution_langs() :
    data = get_all_data(['language'])
  
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

    print df
   
    colors = ['b', 'c', 'y', 'm', 'r']
    pie = df['count'].plot.pie(colors=colors,labels=df['language'], autopct='%1.1f%%')
    

    plt.title('Distribution of Languages')
    plt.show()
    fig = pie.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', 'lang_distribution.png'))

distribution_langs() 
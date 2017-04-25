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
    #plt.legend()
    plt.show()
    fig = box.get_figure()
    fig.savefig(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'Figures', save_to_filename))
  

general_box_plot('cloc', 'box_plot_cloc_total.png', 'Lines of Code', 'Lines of Code, all competitions' )
general_box_plot('exe_size', 'box_plot_exe_size_total.png', 'Size of Executable File', 'Size of Executable, all competitions')
general_box_plot('max_RAM', 'box_plot_memory_total.png', 'Memory footprint (Bytes)', 'Memory footprint, all competitions')
general_box_plot('wall_clock', 'box_plot_wall_cloc_total.png', 'Wall Clock', 'Wall Clocl, all competitions' )
general_box_plot('user_time', 'box_plot_user_time_total.png', 'User Time', 'User Time, all competitions' )
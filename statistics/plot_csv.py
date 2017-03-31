import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *



def test_pandas():
    cid_frame = pandas.read_csv(os.path.join(get_HOME_PATH(),'GCJ-backup','cid_pid_map_new.csv'))
    print cid_frame


def plot_cloc():
    for p_id in get_PROBLEM_IDS(gcj_path):
        for x in range(0,1):
            path_to_cloc = os.path.realpath(os.path.join(get_HOME_PATH(),'GCJ-backup',p_id+'.csv'))
            x = []
            y = []
            languages = get_LANGUAGE()
            with open(path_to_cloc,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter=',')
                next(plots, None)  # skip the headers
                for row in plots:
                    if len(row)>0 :
                        x.append(int(row[4]))
                        y.append(languages.index(row[3]))
                    plt.yticks(range(len(languages)),languages)
                    plt.scatter(x,y, label='Cloc ' + p_id)
                    plt.xlabel('cloc')
                    plt.ylabel('Language')
                    plt.title('Interesting Graph\nCheck it out!')
                    plt.legend()
                    plt.show()

test_pandas()

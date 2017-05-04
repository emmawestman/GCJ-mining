import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas
import errno

from stats_help import *



def plot_error():
    data = get_all_data(['language','exit_code'])
    data = data.loc[data['exit_code'] != '-']
    data = data.loc[data['exit_code'] != 0]
    data = data.loc[data['exit_code'] != '0']
    data = data.loc[data['exit_code'] != -1]
    data = data.loc[data['exit_code'] != '-1']
    data = data.apply(pandas.to_numeric, errors='ignore')
    for x,y in data.groupby(['language', 'exit_code'],as_index = False):
        lang,error =  x
        value = y.language.count()
        number = int(error)
        error_str = str(number)
        print error_str
        if error_str == '-15':
            error_str = "Timeout"
        else:
            error_str = os.strerror(number)

        print lang + ' & ' + str (number) +' & ' + error_str + ' & ' + str(value) + ' \\\ '

    #print df
plot_error()

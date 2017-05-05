import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas
import errno

from stats_help import *

def get_error_data(error_column,user_id=None):
    data = get_all_data([error_column,'language',user_id])
    data = data.loc[data[error_column] != '-']
    data = data.loc[data[error_column] != 0]
    data = data.loc[data[error_column] != '0']
    data = data.loc[data[error_column] != -1]
    data = data.loc[data[error_column] != '-1']
    data = data.apply(pandas.to_numeric, errors='ignore')
    return data


def get_rank_user(columns):
    data = pd.DataFrame()
    c_ids = get_CONTEST_IDS()
    for c_id in c_ids:
        print c_id
        path = os.path.join('../..', 'GCJ-backup', c_id+'.csv')
        df = pd.read_csv(path)
        try:
            df = df[columns]
            df['contest_id'] = c_id
            data = data.append(df)
        except KeyError:
            #df = df['language']
            #size = len(df.index)
            #for c in columns:
            #df[c] = ['-']*size
            print 'skiped: ' + p_id
    return data

def plot_error(error_column):
    data = get_error_data(error_column)
    for x,y in data.groupby(['language', error_column],as_index = False):
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

def plot_rank_error():
    error_data = get_error_data(user_id='user_id',error_column = 'exit_code')
    rank_user_data = get_rank_user(['rank','user_id'])
    new_df = pandas.merge(error_data,rank_user_data, on ='user_id')
    print new_df

plot_rank_error()

import csv
import os
import sys
import pandas as pd

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *

def read_csv_file(filename) :
    path = os.path.join('../..', 'GCJ-backup', filename)
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        content = []
        for row in reader:
            content.append(row)
        attr_names = content[0][1:]

        dict = {}
        for row in content[1:] :
            user_id = row[0]
            user_dict = {}
            for idx, a in enumerate(attr_names) :
                user_dict[a] = row[idx +1]
            dict[user_id] = user_dict
        return dict

def write_to_csv_file(filename, dict) :
    path = os.path.join(get_HOME_PATH(), 'GCJ-backup', filename)
    df = pd.DataFrame.from_dict(dict, orient='index')
    df.index.name('user_id')
    df.to_csv(path)

def write_dict_to_file(filename, problem_id_contest_id_dict):
    path = os.path.join(get_HOME_PATH(), 'GCJ-backup', filename)
    contest_ids = problem_id_contest_id_dict.keys()
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        for contest_id in contest_ids:
            row =[]
            row.append(contest_id)
            for problem_id in problem_id_contest_id_dict[contest_id]:
                row.append(problem_id)
            writer.writerow(row)

def read_csv_file_to_dict(filename):
    path = os.path.join(get_HOME_PATH(), 'GCJ-backup', filename)
    with open(path, 'r') as csvfile:
        writer = csv.reader(csvfile, delimiter=',', quotechar='|')
        dict = {}
        for row in writer :
            dict[row[0]] = row[1:]
    return dict

def get_user_ids(c_id) :
    dict = init_csv(c_id)
    new_dict = {}
    p_ids = dict.keys();
    for id_ in p_ids :
        p_dict = dict [id_]
        new_dict [id_] = p_dict['user_ids']
    return new_dict

def change_column(c_id, p_id, users, column_name, new_values) :
    filename = str(c_id) + '_' + str(p_id) + '.csv'
    dict = read_csv_file(filename)
    for idx, u in enumerate(users) :
        user_dict = dict[u]
        user_dict[column_name] = new_values[idx]
    write_to_csv_file(filename, dict)

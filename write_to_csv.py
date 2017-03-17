import csv
import os
import sys

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
    users = dict.keys()
    attr_names = dict[users[0]].keys()
    first_row = ['user_id'] + attr_names
    matrix = []
    matrix.append(first_row)
    for u in users :
        values = dict[u].values()
        row = [u] + values
        matrix.append(row)
    with open(path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        for row in matrix:
           writer.writerow(row)

def write_dict_to_file(filename, problem_id_contest_id_dict):
    path = os.path.join(get_HOME_PATH(), 'GCJ-backup', filename)
    problem_ids = problem_id_contest_id_dict.keys()
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        for problem in problem_ids:
            row =[]
            row.append(problem)
            row.append(problem_id_contest_id_dict[problem])
            writer.writerow(row)

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

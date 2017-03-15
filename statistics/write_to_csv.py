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
        print attr_names

        dict = {}
        print content
        for row in content[1:] :
            user_id = row[0]
            print user_id
            user_dict = {}
            for idx, a in enumerate(attr_names) :
                print user_dict
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
    with open(path, 'w') as csvfile:
	    writer = csv.writer(csvfile, delimiter=',', quotechar='|')
	    for row in matrix:
	       writer.writerow(row)


def init_csv(p_id) :
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + str(p_id)))
    dict = {}
    for l in get_LANGUAGE() :
        try :
            old_users = dict['user_ids']
            old_langs = dict ['language']
        except KeyError:
            old_users = []
            old_langs = []
        path_lang = os.path.join(path, l)
        users = os.listdir(path_lang)
        dict['user_ids'] =  old_users + users
        langs =  [l] * len(users)
        dict ['language'] = old_langs + langs
    return dict

def create_init_csv(p_id, dict) :
    complete_name = os.path.join(get_HOME_PATH(), 'GCJ-backup', p_id + '.csv')
    with open(complete_name, 'wb') as csvfile :
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #write header
        user_ids = dict['user_ids']
        langs = dict['language']
        writer.writerow(['user_id', 'language'])
        for idx, u in enumerate(user_ids) :
            result = [u, langs[idx]]
            writer.writerow(result)

def change_column(c_id, p_id, users, column_name, new_values) :
    filename = str(c_id) + '_' + str(p_id) + '.csv'
    dict = read_csv_file(filename)
    for idx, u in enumerate(users) :
        user_dict = dict[u]
        user_dict[column_name] = new_values[idx]
    write_to_csv_file(filename, dict)

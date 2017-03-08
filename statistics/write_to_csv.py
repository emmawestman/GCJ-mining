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
	    reader = csv.reader(csvfile, delimiter=' ', quotechar=',')
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
    path = os.path.join('../..', 'GCJ-backup', filename)
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
	    writer = csv.writer(csvfile, delimiter=' ', quotechar=',')
	    for row in matrix:
	       writer.writerow(row)

def get_user_ids(c_id) :
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id))
    dict = {}
    for l in get_LANGUAGE() :            
        path_lang = os.path.join(path, l)
        prob_ids = os.listdir(path_lang)
        for p_id in prob_ids :
            users = os.listdir(os.path.join(path_lang, p_id))
            try :
                old_users = dict [p_id]
            except KeyError:
                old_users = []
            dict [p_id] =  old_users.append(users)

        print dict

def create_csv(c_id) :
        path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id))
        user_ids = []
        for l in get_LANGUAGE() :
            path_lang = os.path.join(path, l)
            prob_ids = os.listdir(path_lang)
            for p_id in prob_ids :
                users = os.listdir(os.path.join(path_lang, p_id))
                print os.path.join(path_lang, p_id)
                print users
                user_ids.append(users)

        print user_ids

        complete_name = os.path.join('../..', 'GCJ-backup', c_id + '_' + p_id + '.csv') 
        with open(complete_name, 'wb') as csvfile :
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)  
            #write header
            writer.writerow(['user_id'])
            for u in user_ids :
                result = [u]
                writer.writerow(result)

def change_column(c_id, p_id, users, column_name, new_values) : 
    filename = c_id + '_' + p_id + '.csv'
    dict = read_csv_file(filename)
    for idx, u in enumerate(users) :
        user_dict = dict[u]
        user_dict[column_name] = new_values[idx]
    write_to_csv_file(filename, dict)
	

get_user_ids('11254486')	
#create_csv('11254486')
'''
print read_csv_file('c123_p123.csv')
change_column('c123', 'p123', ['user1', 'user2', 'user3', 'user4', 'user5'], 'lang', ['C++', 'C++', 'Python', 'java', 'C++'])
print read_csv_file('c123_p123.csv')
change_column('c123', 'p123', ['user1', 'user2', 'user3', 'user4', 'user5'], 'compiler', ['-', '-', '3.5', '-', '-'])
print read_csv_file('c123_p123.csv')
'''





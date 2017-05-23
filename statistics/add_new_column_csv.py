import os
import sys
import re


gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *


def add_error_msg_column_csv() :
    for p_id in get_PROBLEM_IDS(gcj_path) :
        print p_id
        filename = p_id + '.csv'
        dict = read_csv_file(filename)
        users = dict.keys()
        for u in users :
            user_dict = dict[u]
            user_dict['compile_error_msg'] = '-'
            user_dict['run_error_msg'] = '-'
        write_to_csv_file(filename, dict)

#add_error_msg_column_csv()

def change_file_names():
	path = os.path.join(os.getcwd(), '../../datacollection')
	sfs = os.listdir(path)
	solutions_folders = []
	for sf in sfs :
		if not '.' in sf :
			solutions_folders.append(sf)
	for sf in solutions_folders :
		lang_path = os.path.join(path, sf)
		langs = os.listdir(lang_path)
		for lf in langs :
			user_path = os.path.join(lang_path, lf)
			user_dirs = os.listdir(user_path)
			for user in user_dirs :
				file_path = os.path.join(user_path, user)
				files = os.listdir(file_path)
				for f in files:
					if ' '  in f:
						print 'changing name of: ' + f
						file_ending = f.split('.')[1]
						src = os.path.join(file_path, f)
						dst = os.path.join(file_path, 'solution.'+file_ending)
						print src
						print dst
						os.rename(src, dst)
						


change_file_names()
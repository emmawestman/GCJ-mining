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

add_error_msg_column_csv()
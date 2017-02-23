from constants import *
import os
from datetime import datetime
from compile_support_module import remove_all_old_files


# function to count the number if downloaded files
# problem_id, language, nbr_of_files

languages = get_LANGUAGE()
contest_ids = ['1128486', '2984486']#get_CONTEST_IDS()

def count(c_id, lang) :
	countfile = open('nbr_of_files.txt', "a")
	now = str(datetime.now())
	countfile.write(now + '\n')
	countfile.write(c_id + '\n')

	path = os.path.realpath(os.path.join('..','solutions_' + c_id, lang ))
	directories = os.listdir(path)
	print directories 
	for root, dirs, files in os.walk(path):
		print dirs
		# get p_id
		nbr = 0
		for f in files:
			print f
			this_file_ending = f.split('.')[1]
			this_file_ending = '.' + this_file_ending
			if any (e == this_file_ending for e in get_FILE_ENDING(lang)):
				nbr += 1
		countfile.write(lang + '\t' + 'nbr of files: ' + str(nbr) + '\n')
	countfile.close()

def test_any(f):
	fe = ['.cpp', '.c++', '.cxx']
	ffe = f.split('.')[1]
	ffe = '.' + ffe
	print ffe
	if any (e == ffe for e in fe):
		print True

def count_everything():
	for c_id in contest_ids :
		for l in languages :
			count(c_id, l)

remove_all_old_files()
count_everything()








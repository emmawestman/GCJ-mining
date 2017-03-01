from constants import *
import os
from datetime import datetime
from compile_support_module import remove_all_old_files


# function to count the number if downloaded files
# problem_id, language, nbr_of_files

languages = get_LANGUAGE()
contest_ids = get_CONTEST_IDS()



def count_everything():
	countfile = open('nbr_of_files.txt', "a")
	now = str(datetime.now())
	countfile.write(now + '\n')
	
	for c_id in contest_ids:
		print 'Counting for contest id ' + c_id + '...'
		countfile.write('\n')
		countfile.write('Contest id: ' + c_id + '\n')
		for l in languages:
			print 'Counting for contest language ' + l + ' in ' + c_id + '...'
			path = os.path.realpath(os.path.join('..','solutions_' + c_id, l))
			p_ids = os.listdir(path)
			nbr = 0	
			for p_id in p_ids:
				if p_id in os.listdir(path) :
					p_id_path = os.path.join(path, p_id)
					nbr = len(os.listdir(p_id_path))
				countfile.write(l + '\t' + p_id + '\t' + 'nbr of files: ' + str(nbr) + '\n')
	countfile.close()



remove_all_old_files()
count_everything()


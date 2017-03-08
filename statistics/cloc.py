import os
import subprocess
from write_to_csv import *

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *

LANGUAGE = get_LANGUAGE()


# creates on row with prob_id, langage, user, blank, comment, code
def cloc_problem(c_id, prob_id, lang, user) :
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + str(c_id), lang, prob_id, user))
	print path
	cmd = ['cloc ' + path ]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	data = [int(s) for s in output.split() if s.isdigit()]
	if len(data) != 3 :
		result =  [str(data[4]), str(data[5]), str(data[6])]
		print result
	else :
		result = ['-', '-', '-']
		print result
	return result

# creates a file containing rows with the format describen in cloc_problem
def cloc_contest(c_id) :
	print 'CLOC for ' + str(c_id)
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + str(c_id)))
	results = []
	prob_ids = []
	all_user_ids = get_user_ids(c_id)
	for l in LANGUAGE :
		path_lang = os.path.join(path, l)
		prob_ids = os.listdir(path_lang)
		for p_id in prob_ids :
			users = os.listdir(os.path.join(path_lang, p_id))
			for user in users :
				results.append(cloc_problem(c_id, p_id, l, user))
				#user_ids.append(users)
				# write to csv
	for p_id in prob_ids :
		user_ids = all_user_ids [p_id]
		print user_ids
	 	change_column(c_id, p_id, user_ids, 'cloc', [row[2] for row in results])
		change_column(c_id, p_id, user_ids, 'blanks', [row[0] for row in results])
		change_column(c_id, p_id, user_ids, 'coments', [row[1] for row in results])


# calcualte cloc for all contests
def cloc_all() :
	for c_id in get_CONTEST_IDS() :
		cloc_contest(c_id)

cloc_all()

import os
import subprocess
from write_to_csv import *

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *

LANGUAGE = get_LANGUAGE()


# creates on row with prob_id, langage, user, blank, comment, code
def cloc_file(prob_id, lang, user) :
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + prob_id, lang, user))
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
def cloc_problem(p_id) :
	print 'CLOC for ' + str(p_id)
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + str(p_id)))
	prob_ids = []
	dict = {}
	for l in LANGUAGE :
		path_lang = os.path.join(path, l)
		try :
			prob_dict = dict [p_id]
		except KeyError:
			prob_dict = read_csv_file(str(p_id) + '.csv')
			dict[p_id] = prob_dict
		users = os.listdir(path_lang)
		for user in users :
			results = (cloc_file(p_id, l, user))
			# update user dict
			user_dict = prob_dict[user]
			user_dict['cloc'] = results[2]
			user_dict['blanks'] = results[0]
			user_dict['comments'] = results[1]
	# write to dict to file
	write_to_csv_file(str(p_id) + '.csv', dict)





# calcualte cloc for all contests
def cloc_all() :
	# one dir up
	one_up = os.path.join(os.getcwd(), '../')
	for problem_id in get_PROBLEM_IDS(one_up):
		cloc_problem(problem_id)

cloc_all()

import os
import subprocess
import csv
from constants import *

LANGUAGE = get_LANGUAGE()


# creates on row with prob_id, langage, user, blank, comment, code
def cloc_problem(c_id, prob_id, lang, user) :
	path = os.path.realpath(os.path.join('..','solutions_' + c_id, lang, prob_id, user))
	cmd = ['cloc ' + path ]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	data = [int(s) for s in output.split() if s.isdigit()]
	result = [prob_id , lang, user, str(data[4]), str(data[5]), str(data[6])]
	return result

# creates a file containing rows with the format describen in cloc_problem
def cloc_contest(c_id) :
	# create file to store data in
	complete_name = os.path.join('..', 'GCJ-backup', 'cloc_' + c_id + '.csv')         
	with open(complete_name, 'wb') as csvfile :
		writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		path = os.path.realpath(os.path.join('..','solutions_' + c_id))
		for l in LANGUAGE :
			path_lang = os.path.join(path, l)
			prob_ids = os.listdir(path_lang)
			for p_id in prob_ids :
				users = os.listdir(os.path.join(path_lang, p_id))
				for user in users :
					result = cloc_problem(c_id, p_id, l, user)
					writer.writerow(result)

# calcualte cloc for all contests
def cloc_all() :
	for c_id in get_CONTEST_IDS() :
		cloc_contest(c_id)

cloc_all()
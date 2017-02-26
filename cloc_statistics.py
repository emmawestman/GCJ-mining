# file to test to read csv files back into python and 
# do som simple statistics
import csv
import os
from constants import *
from compile_support_module import *

def read_csv_file(filename) :
	path = os.path.join('..', 'GCJ-backup', filename)
	print path
	with open(path, 'rb') as csvfile:
	    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	    content = ""
	    for row in reader:
	        content +=  ', '.join(row) +'\n'
	    return content


def group_by(content) :
	groups = []
	lang = get_LANGUAGE()
	rows = content.split("\n") 
	prob_ids = []
	# remove last row which is blank.... don't know why last row is blank...
	rows = rows[:len(rows) -1]
	for row in rows :
		id_ = row.split(',')[0]
		if id_ not in prob_ids :
			prob_ids.append(id_)

	for p_id in prob_ids :
		for l in lang :
			group = [r for r in rows if p_id + ', ' + l + ',' in r]
			if group != [] :
				groups.append(group)

	return groups

def verify_groups(groups) :
	for g in groups :
		items = []
		if g != [] :
			for row in g :
				item = row.split(',')
				items.append(item)
			p_id = items[0][0]
			l = items[0][1]
			flag = True
			for item in items :
				if item[0] == p_id and item[1] == l :
					flag = flag and True
				else :
					#print 'found false statement'
					flag = False
			
			print flag





def count_avg(group) :
	for g in group :
		blank = 0
		comment = 0
		code = 0
		p_id = ''
		language = ''
		size = len(g)
		for row in g :
			elements = row.split(',')
			p_id = elements[0]
			language = elements[1]
			blank += int(elements[3])
			comment += int(elements[4])
			code += int(elements[5])
		print p_id + ' ' + language + ' ' + str(blank/size) + ' ' + str(comment/size) + ' ' + str(code/size)
		return [p_id, language, str(blank/size), str(comment/size), str(code/size)]


def avg_all() :
	c_ids = get_CONTEST_IDS()
	for c_id in c_ids :
		content = read_csv_file('cloc_' + c_id + '.csv')
		groups = group_by(content)
		#verify_groups(groups)
		result = count_avg(groups)
		complete_name = os.path.join('..', 'GCJ-backup', 'cloc_avg_' + c_id + '.csv') 
		with open(complete_name, 'wb') as csvfile :
			writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(result)


def clean_dirs():
	c_ids = get_CONTEST_IDS()
	languages = get_LANGUAGE()
	for c_id  in c_ids :
		for l in languages :
			remove_old_files(l, c_id)

clean_dirs()
avg_all()


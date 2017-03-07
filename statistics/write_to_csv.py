import csv 
import os


def read_csv_file(filename) :
	path = os.path.join('../..', 'GCJ-backup', filename)
	with open(path, 'rb') as csvfile:
	    reader = csv.reader(csvfile, delimiter=' ', quotechar=',')
	    content = ""
	    for row in reader:
	        content +=  ', '.join(row) +'\n'
	    return content

def write_to_csv_file(filename, matrix) :
	path = os.path.join('../..', 'GCJ-backup', filename)
	with open(path, 'wb') as csvfile:
	    writer = csv.writer(csvfile, delimiter=' ', quotechar=',')
	    for row in matrix:
	       writer.writerow(row)


def create_csv(c_id, p_id, users, lang) :
	complete_name = os.path.join('../..', 'GCJ-backup', c_id + '_' + p_id + '.csv') 
	with open(complete_name, 'wb') as csvfile :
		writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)  
		#write header
		writer.writerow(['username', 'rank', 'lang'])
		i = 1 
		for u in users :
			result = [u, i, lang]
			writer.writerow(result)
			i += 1

def change_column(c_id, p_id, username, column, new_value) : 
	filename = c_id + '_' + p_id + '.csv'
	content = read_csv_file(filename)
	lines = content.split('\n')
	matrix = [l.split(',') for l in lines]
	new_lines = []
	## find row of user
	for l in lines :
		attributes = l.split(',')
		if attributes[0] == username :	
			#edit row
			attributes[column] = new_value
		new_lines.append(attributes)
	write_to_csv_file(filename, new_lines)
	
	#writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	#writer.writerow(result)
	
create_csv('c123', 'p123', ['user1', 'user2', 'user3', 'user4', 'user5'], 'C++')
change_column('c123', 'p123', 'user4', 2, 'java')





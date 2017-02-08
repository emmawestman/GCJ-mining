import os
import shutil
from stuff_module import create_folder

PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))

def filter_substring(error_message_start,error_message_end,error_string):
	indexes = []
	start_index =error_string.find(error_message_start)
	end_index = error_string.find(error_message_end)
	indexes.append(start_index)
	indexes.append(end_index)
	print "START INDEX " + str(start_index)
	print "END INDEX " + str(end_index)
	return indexes

def get_input_file(problem_folder):
	problem_input = [f for f in os.listdir(PATH_INPUT) if (f.split('.')[0]==problem_folder)]
	return problem_input[0]

def rename_file(user_path,path_to_file,old_file_name,new_file_name):
	curr_path = user_path
	if new_file_name.find('/') !=-1:
		path_to_create_folder = new_file_name.split('/')
		new_file_name = path_to_create_folder[-1]
		lim = len(path_to_create_folder)-1
		for x in range(0,lim):
			print 'in for loop'
			name = path_to_create_folder[0]
			create_folder(name)
			print 'created folder'
			curr_path = os.path.join(curr_path,name) 
			os.chdir(curr_path)
	shutil.copy(os.path.join(path_to_file,old_file_name),curr_path)
	print "OLD NAME "
	os.chdir(curr_path) 
	os.rename(old_file_name,new_file_name)
	os.chdir(user_path)	

def find_namespace(filename, path):
	full_path = os.path.join(path, filename)
	file1 = open(full_path, "r")
	content = file1.read()
	index_start = content.find('namespace ') + len('namespace ')
	content = content[index_start:]
	index_end = content.find('\n')
	namespace = content[:index_end]
	return namespace



def remove_old_files(language,language_path):
	for root, dirs, files in os.walk(language_path):
		filelist = [ f for f in files if not(f.endswith(language)) ]
		for f in filelist:			
			os.remove(os.path.join(root,f))

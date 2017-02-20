import os
import shutil
from stuff_module import create_folder
import re



def get_input_file(problem_folder, PATH_INPUT):
	problem_input = [f for f in os.listdir(PATH_INPUT) if (f.split('.')[0]==problem_folder)]
	return problem_input[0]

def rename_file(user_path,path_to_file,old_file_name,new_file_name):
	curr_path = user_path
	if new_file_name.find('/') !=-1:
		path_to_create_folder = new_file_name.split('/')
		new_file_name = path_to_create_folder[-1]
		lim = len(path_to_create_folder)-1
		for x in range(0,lim):
			name = path_to_create_folder[0]
			create_folder(name)
			curr_path = os.path.join(curr_path,name) 
			os.chdir(curr_path)
	shutil.copy(os.path.join(path_to_file,old_file_name),curr_path)
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

def find_out_what_regex(regex,file_contents):
	found_matches = re.search(regex,file_contents)
	if found_matches is not None:
		match = found_matches.group(0)
		return match
	return None


def rename_stuff_in_file(new_stuff,old_stuff,file_contents,counter):
	#read old content
	#change to the "right module name"
	if (counter == 0):
		file_contents= re.sub(old_stuff,new_stuff,file_contents)
	else :
		file_contents= re.sub(old_stuff,new_stuff,file_contents,counter)
	return file_contents

def get_contents_of_file(file_path):
	file_manager = open(file_path,'r')
	file_contents = file_manager.read()
	file_manager.close()
	return file_contents,file_manager

def write_new_contents_to_the_file(file_path,file_contents):
	#write changes
	file_manager=open(file_path,'w')
	file_manager.write(file_contents)
	file_manager.close()

#language is the file ending for the language
def remove_old_files(language, c_id):
	language_path = os.path.realpath(os.path.join('..','solutions_' + c_id, language))
	for root, dirs, files in os.walk(language_path):
		if language == 'C++' or language == 'C':
			# remove executable files for c++ an c
			filelist = [f for f in files if '.' not in f]
		else:
			filelist = [ f for f in files if not(f.endswith(language)) ]
		# remove extra created main files
		if language == 'C#':
			filelist = [ f for f in files if (f == 'TestMain.cs' or f.endswith('.exe')) ]
			for file in filelist:
				os.remove(os.path.join(root,file))



def get_compile_info(regexp, root, f):
	index = root.find(regexp)
	filename = root[index+len(regexp):]
	index = filename.find('/')
	user = filename[index+1:]
	index = f.find('.')
	name = f[:index]
	return user, name

def get_run_info(regexp, root):
	index = root.find(regexp)
	filename = root[index+len(regexp)+1:]
	index = filename.find('/')
	user = filename[index+1:]
	filename = filename[:index]	
	input_file = filename + '.in' 	
	return user, input_file


def check_exit_code():
	cmd = ['echo $?']
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return output
	







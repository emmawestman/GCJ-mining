import os
import shutil
from stuff_module import create_folder

PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))



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


 
def rename_stuff_in_file(new_stuff,old_stuff,file_path):
	#read old content
	file_manager = open(file_path,'r')
	file_contents = file_manager.read()
	file_manager.close()
	#change to the "right module name"
	file_contents= re.sub(old_stuff,new_stuff,file_contents)
	#write changes
	file_manager=open(file_path,'w')
	file_manager.write(file_contents)
	file_manager.close()




def remove_old_files(language,language_path):
	for root, dirs, files in os.walk(language_path):
		filelist = [ f for f in files if not(f.endswith(language)) ]
		for f in filelist:			
			os.remove(os.path.join(root,f))

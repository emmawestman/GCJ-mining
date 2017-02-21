from compile_support_module import *
from finding_regexes import *
import re
from shutil import copyfile
from compile_python import *

def handle_python_2x_errors(file_path,path_input,c_id,root,errors):
	error_name = get_error_name(errors)
	if error_name =='ImportError':
		flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip')
		if flag == 0:
			return run_python_3x(file_path,path_input,c_id,root)
		return run_python_2x(file_path,path_input,c_id,root)	
	elif error_name == 'SyntaxError':
		return run_python_3x(file_path,path_input,c_id,root)
	elif error_name =='FileNotFoundError' or error_name == 'IOError':
		handle_file_not_found(path_input,root,c_id,file_path)
		return run_python_2x(file_path,path_input,c_id,root)
	elif error_name == 'IndexError':
		handle_file_not_found(path_input,root,c_id,file_path)
		ret_flag = run_python_2x(file_path,path_input,c_id,root)
		return ret_flag
	print errors
	return 0

def handle_python_3x_errors(errors_name,errors,file_path,path_input):
	if error_name =='ImportError':
		flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip3')
		if flag == 1:
			return run_python_3x(file_path,path_input,c_id,root)
		remove_module_name(missing_module_name,file_path)
	elif error_name =='FileNotFoundError' or error_name =='IOError':
		handle_file_not_found(path_input,root,c_id,file_path)
		return run_python_3x(file_path,path_input,c_id,root)
	return 0

		
def get_error_name (errors):
	error_list = filter_information('\w+Error',None,errors)
	if len(error_list)>0:
		error_name = error_list[0]
		return error_name
	return errors 


def handle_import_error(file_path,path_input,pip_version):
	missing_module_name = find_missing_module_name(errors)
	if missing_module_name == 'run':
		rename_stuff_in_file('runpy','run',file_path,1)
	else :
		pip_errors = pip_install_module(pip_version,missing_module_name)
		if len(pip_errors)>0:
			print pip_errors
			return 0,missing_module_name
	return 1,None


def handle_file_not_found(input_file,root,c_id,file_path):
	file_contents = get_contents_of_file(file_path)
	changed_content = rename_input_file(file_contents,input_file)
	#write_new_contents_to_the_file(file_path,changed_content) # write changes to the python file
	#file_contents = get_contents_of_file(file_path)
	changed_contents = rename_output_file(file_contents,root)
	write_new_contents_to_the_file(file_path,changed_contents)



def create_a_copy_of_input_file(c_id,input_file):
	dst = input_file + '(1)'
	number_of_files = len(os.listdir(PATH_INPUT+c_id)) 
	copyfile(input_file, dst) #create a copy of input file
	return dst,number_of_files

#dictionary for old- new regex pairs
def get_old_new_regex_dict(input_file):
	return {'open\((.*[\'\"]r[\'\"])\)':'open (\'' + input_file + '\''+ ',' +' \'r\')',
		'with open\((.*?)\)':'with open (\'' + input_file + '\''+ ',' +' \'r\')',
		'file\(.*?\)':'file(\'' + input_file +'\')',
		'open\((.*?)\)':'\'' + input_file +'\''}

def find_old_new_regex(file_contents,input_file):
	regex_dict = get_old_new_regex_dict(input_file)
	for key, value in regex_dict.iteritems():
		old_regex = find_out_what_regex(key,file_contents)
		if old_regex is not None:
			return old_regex,value

def rename_input_file(file_contents,input_file):
	old_regex,new_regex = find_old_new_regex(file_contents,input_file)
	new_content = file_contents.replace(old_regex,new_regex)
	return new_content

def rename_output_file(file_contents,root): 
	old_regex = re.findall('open\(.*[\'\"]w[\'\"]\)',file_contents) # find out what regex
	if len(old_regex) > 0:
		old_regex = old_regex[0]
		new_regex = 'open(\'' +  os.path.join(root,'output.txt') + '\'' + ',' + '\'w\')'
		file_contents = file_contents.replace(old_regex,new_regex)
	return file_contents


def remove_copy_of_input_file(number_of_files,dst,root,c_id):
	return 0

def find_missing_module_name(errors):
	missing_module_name = find_out_what_regex('named\s(\w+)',errors)
	missing_module_name = missing_module_name.replace('named ','')
	if missing_module_name is None :
		missing_module_name = find_out_what_regex('from\s(\w+)\simport',errors)
		print "missing module name " + missing_module_name
		missing_module_name = missing_module_name.replace('from ','')
		missing_module_name = missing_module_name.replace(' import','')
	return missing_module_name

import os
import subprocess
from handle_python_errors import *
import sys

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *

PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(),'input_'))


def compile_python(p_id, dict):
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + p_id, 'Python' ))
	print path
	input_path = PATH_INPUT + p_id
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith('.py'):
				nbr_of_files += 1
				filename = get_input_file(root)+'.in'
				path_file = os.path.join(root,f)
				path_input = os.path.join(input_path,filename)
				succes_of_file, dict = run_python_2x(path_file,path_input,p_id,root, dict)
				# update dict compiled YES/NO
				user_id = get_user_id(path_file)
				user_dict = dict[user_id]
				if succes_of_file == 1 :
					user_dict['compiled'] = 'YES'
				else :
					user_dict['compiled'] = 'NO'
				succes_nbr += succes_of_file
	return succes_nbr, nbr_of_files, dict



def run_python_2x(file_path,path_input,p_id,root, dict):
	print "Running file python " + file_path
	args = ' < ' + path_input
	errors, dict = run_python_command('python ',file_path, args, dict)
	if len(errors) > 0:
		return handle_python_2x_errors(file_path,path_input,p_id,root,errors,dict) 			
	return 1, dict


def run_python_3x(file_path,path_input,p_id,root,dict):
	print "Running file python3 " + file_path
	args = ' < ' + path_input
	errors, dict = run_python_command('python3 ',file_path, args, dict)
	if len(errors) > 0:
		return handle_python_3x_errors(errors,file_path,path_input,p_id,root,dict)
	return 1, dict

def run_python_command(pythonversion,path_file,args,dict):	
	# update dictonry so verison is stored in csv
	user_id = get_user_id(path_file)
	user_dict = dict[user_id]
	if pythonversion == 'python3 ' :
		version = "3.5"
	else:
		version = "2.7"
	user_dict['compiler_version'] = version

	cmd = [pythonversion + path_file + args]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors, dict

def handle_python_2x_errors(file_path,path_input,p_id,root,errors,dict):
	error_name = get_error_name(errors)
	if error_name =='ImportError':
		flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip')
		if flag == 0:
			return run_python_3x(file_path,path_input,p_id,root,dict)
		return run_python_2x(file_path,path_input,p_id,root)	
	elif error_name == 'SyntaxError':
		return run_python_3x(file_path,path_input,p_id,root,error, dict)
	elif error_name =='FileNotFoundError' or error_name == 'IOError':
		handle_python_file_not_found(path_input,root,p_id,file_path)
		return run_python_2x(file_path,path_input,p_id,root,dict)
	elif error_name == 'IndexError':
		args = ' ' + path_input +' '+os.path.join(root,'output.txt')
		errors,dict = run_python_command('python ',file_path,args,dict)
		if len(errors) == 0:
			return 1, dict
	print errors
	return 0, dict

def handle_python_3x_errors(errors,file_path,path_input,p_id,root,dict):
	error_name = get_error_name(errors)
	if error_name =='ImportError':
		flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip3')
		print 'handle python 3: ' + missing_module_name
		if flag == 1:
			return run_python_3x(file_path,path_input,p_id,root,dict)
	elif error_name =='FileNotFoundError' or error_name =='IOError':
		handle_python_file_not_found(path_input,root,p_id,file_path)
		run_python_3x(file_path,path_input,p_id,root,dict)
	print errors
	return 0, dict


import os
import subprocess
from handle_python_errors import *

PATH_INPUT = os.path.realpath(os.path.join('..','input_'))


def compile_python(c_id):
	path = os.path.realpath(os.path.join('..','solutions_' + c_id, 'Python' ))
	input_path = PATH_INPUT + c_id
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith('.py'):
				nbr_of_files += 1
				filename = get_input_file(root)+'.in'
				path_file = os.path.join(root,f)
				print "Running file " + path_file
				path_input = os.path.join(input_path,filename)
				succes_nbr += run_python_2x(path_file,path_input,c_id,root)
	return succes_nbr, nbr_of_files



def run_python_2x(file_path,path_input,c_id,root):
	errors = run_python_commando('timeout 30s python ',file_path,path_input)
	if len(errors) > 0:
		return handle_python_2x_errors(file_path,path_input,c_id,root,errors)			
	return 1


def run_python_3x(file_path,path_input,c_id,root):
	errors = run_python_commando('timeout 30s python3 ',file_path,path_input)
	if len(errors) > 0:
		return handle_python_3x_errors(errors,file_path,path_input,c_id,root)
	return 1

def run_python_commando(pythonversion,path_file,path_input):	
	cmd = [pythonversion + path_file + ' < ' + path_input]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

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

def handle_python_3x_errors(errors,file_path,path_input):
	error_name = get_error_name(errors)
	if error_name =='ImportError':
		flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip3')
		if flag == 1:
			return run_python_3x(file_path,path_input,c_id,root)
		remove_module_name(missing_module_name,file_path)
	elif error_name =='FileNotFoundError' or error_name =='IOError':
		handle_file_not_found(path_input,root,c_id,file_path)
		return run_python_3x(file_path,path_input,c_id,root)
	print errors
	return 0

def handle_python_3x_errors(errors,file_path,path_input):
	error_name = get_error_name(errors)
	if error_name =='ImportError':
		flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip3')
		if flag == 1:
			return run_python_3x(file_path,path_input,c_id,root)
		remove_module_name(missing_module_name,file_path)
	elif error_name =='FileNotFoundError' or error_name =='IOError':
		handle_file_not_found(path_input,root,c_id,file_path)
		return run_python_3x(file_path,path_input,c_id,root)
	print errors
	return 0

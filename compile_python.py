import os
import subprocess
from compile_support_module import *
from finding_regexes import *
import re
from handle_python_errors import *
from shutil import copyfile

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
	errors = run_python_commando('python ',file_path,path_input)
	if len(errors) > 0:
		return handle_python_2x_errors(file_path,path_input,c_id,root,errors)			
	return 1


def run_python_3x(file_path,path_input,c_id,root):
	errors = run_python_commando('python3 ',file_path,path_input)
	if len(errors) > 0:
		error_list = filter_information('\w+Error',None,errors)
		if len(error_list)>0:
			error_name = error_list[0]			
			return handle_python_3x_errors(error_name,errors,file_path,path_input,c_id,root)
		print errors
		return 0
	return 1

def pip_install_module(pip_version,module_name):
	cmd = [pip_version + ' install ' + module_name]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

def run_python_commando(pythonversion,path_file,path_input):	
	cmd = [pythonversion + path_file + ' < ' + path_input]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors





import os
import subprocess
from compile_support_module import *
from finding_regexes import *
import re




def compile_python(c_id):
	path = os.path.realpath(os.path.join('..','solutions_' + c_id, 'Python' ))
	PATH_INPUT = os.path.realpath(os.path.join('..','input_' + c_id))
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith('.py'):
				nbr_of_files += 1
				print nbr_of_files
				filename = get_input_file(root) + '.in'
				path_file = os.path.join(root,f)
				print "File name " + filename
				path_input = os.path.join(PATH_INPUT,filename)
				succes_nbr += run_python_2x(path_file,path_input)
	return succes_nbr, nbr_of_files

def get_input_file(root):
	return re.search('\d+\_\d', root).group(0)

def run_python_2x(file_path,path_input):
	errors, exit_code = run_python_commando('timeout 120s python ',file_path,path_input)
	print exit_code
	if int(exit_code) == 0:	
		if len(errors) > 0:
			error_list = filter_information('\w+Error',None,errors)
			if len(error_list)>0:
				error_name = error_list[0]			
				if error_name =='ImportError':
					error_code = handle_import_error(file_path,path_input,errors,'pip')
					if error_code == 1:
						return run_python_2x(file_path,path_input)
				elif error_name == 'SyntaxError':
					return run_python_3x(file_path,path_input)
			print errors
			return 0
		return 1
	else:
		return 0
		print 'command timedout'

def handle_import_error(file_path,path_input,errors,pip_version):
	missing_module_name = filter_information('named\s\w+',None,errors)[0]
	missing_module_name = missing_module_name.replace('named','')
	if missing_module_name == 'devtools':
		rename_stuff_in_file('','import devtools',file_path)
	elif missing_module_name == 'run':
		rename_stuff_in_file('runpy','run',file_path)
	else :
		pip_errors = pip_install_module(pip_version,missing_module_name)
		if len(pip_errors)>0:
			print pip_errors
			return 0
	return 1


def run_python_3x(file_path,path_input):
	errors, exit_code = run_python_commando('timeout 120s python3 ',file_path,path_input)
	if int(exit_code) == 0:	
		if len(errors) > 0:
			error_list = filter_information('\w+Error',None,errors)
			if len(error_list)>0:
				error_name = error_list[0]			
				if error_name =='ImportError':
					error_code = handle_import_error(file_path,path_input,errors,'pip3')
					if error_code == 1:
						return run_python_3x(file_path,path_input)
			print errors
			return 0
		return 1
	else:
		#did not finish within timeout
		return 0
		print 'commad timed out'

def pip_install_module(pip_version,module_name):
	cmd = [pip_version + ' install ' + module_name]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

def run_python_commando(pythonversion,path_file,path_input):
	print path_input	
	cmd = [pythonversion + path_file + ' < ' + path_input + '; echo $?']
	print cmd
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	exit_code = check_exit_code()
	#print exit_code
	output, errors = p.communicate()
	print output
	exit_code = check_exit_code()
	print exit_code
	return errors, exit_code





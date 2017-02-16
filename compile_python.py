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
				regexp = "/Python/"
				index = root.find(regexp)
				filename = root[index+len(regexp):]
				index = filename.find('/')
				user = filename[index+1:]
				filename = filename[:index]
				filename = filename + '.in'
				print filename
				path_file = os.path.join(root,f)
				path_input = os.path.join(PATH_INPUT,filename)
				succes_nbr += run_python_2x(path_file,path_input)
	return succes_nbr, nbr_of_files

def run_python_2x(file_path,path_input):
	errors, exit_code = run_python_commando('timeout 120s python ',file_path,path_input)
	#exit code 0 means cmmand finsined within timeout
	print exit_code	
	if exit_code == 0:
		if len(errors) > 0:
			error_list = filter_information('\w+Error',None,errors)
			if len(error_list)>0:
				error_name = error_list[0]			
				if error_name =='ImportError':
					missing_module_name = filter_information('named\s\w+',None,errors)[0]
					missing_module_name = missing_module_name.replace('named','')
					if missing_module_name == 'devtools':
						rename_stuff_in_file('','import devtools',file_path)
						run_python_2x(file_path,path_input)
					elif missing_module_name == 'run':
						rename_stuff_in_file('runpy','run',file_path)
						run_python_2x(file_path,path_input)
					else :
						pip_errors = pip_install_module(missing_module_name)
						if len(pip_errors>0):
							print pip_errors
							return 0
						else:
							return run_python_2x(file_path,path_input)
				elif error_name == 'SyntaxError':
					return run_python_3x(file_path,path_input)
			print errors
			return 0
		return 1
	else:
		# command did not finish within timeout
		return 0

def run_python_3x(file_path,path_input):
	errors, exit_code = run_python_commando('timeout 120s python3 ',file_path,path_input)
	if exit_code == 0:
		if len(errors) > 0:
			error_list = filter_information('\w+Error',None,errors)
			if len(error_list)>0:
				error_name = error_list[0]			
				if error_name =='ImportError':
					missing_module_name = filter_information('named\s\w+',None,errors)[0]
					missing_module_name = missing_module_name.replace('named','')
					if missing_module_name == 'devtools':
						rename_stuff_in_file('','import devtools',file_path)
						run_python_3x(file_path,path_input)
					elif missing_module_name == 'run':
						rename_stuff_in_file('runpy','run',file_path)
						run_python_3x(file_path,path_input)
					else :
						pip_errors = pip_install_module(missing_module_name)
						if len(pip_errors>0):
							print pip_errors
							return 0
						else:
							return run_python_3x(file_path,path_input)
			else:
				print errors
				return 0
		
		return 1
	else:
		# command did not finish within timeout
		return 0
def pip_install_module(pip_version,module_name):
	cmd = [pip_version + ' install ' + module_name]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

def run_python_commando(pythonversion,path_file,path_input):
	print path_input	
	cmd = [pythonversion + path_file + ' < ' + path_input]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	exit_code = check_exit_code()
	return errors, exit_code





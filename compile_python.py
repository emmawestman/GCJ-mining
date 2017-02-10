import os
import subprocess
from compile_support_module import *
from finding_regexes import *
import re

PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))


def compile_python(path):
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			regexp = "/Python/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			filename = filename[:index]
			filename = filename + '.in'
			path_file = os.path.join(root,f)
			path_input = os.path.join(PATH_INPUT,filename)
			succes_nbr += run_python_2x(path_file,path_input)
	return succes_nbr, nbr_of_files

def run_python_2x(file_path,path_input):
	errors = run_python_commando('python ',file_path,path_input)
	if len(errors) > 0:
		error_list = filter_information('\w+Error',None,errors)
		if not error_list:
			error_name = error_list[0]			
			if error_name =='ImportError':
				missing_module_name = filter_information('named\s\w+',None,errors)[0]
				missing_module_name = missing_module_name.replace('named','')
				if missing_module_name == 'devtools':
					rename_stuff_in_file('','import devtools',file_path)
					run_python_2x(file_path,path_input)
				elif missing_module_name == 'run':
					rename_stuff_in_file('runpy','run',file_path)
					return run_python_2x(file_path,path_input)
				else :
					pip_errors = pip_install_module(missing_module_name)
					if len(pip_errors>0):
						print pip_errors
						return 0
					else:
						return run_python_2x(file_path,path_input)
			elif error_name == 'SyntaxError':
				return run_python_3x(file_path,path_input)
		else:
			print errors
			return 0
	else :
		return 1

def run_python_3x(file_path,path_input):
	errors = run_python_commando('python3 ',file_path,path_input)
	if len(errors) > 0:
		error_list = filter_information('\w+Error',None,errors)[-1]
		if not error_list:			
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
					else:
						return run_python_3x(file_path,path_input)
		else:
			print errors
			return 0
	else :
		return 1
 
def rename_stuff_in_file(new_module_name,old_module_name,file_path):
	#read old content
	file_manager = open(file_path,'r')
	file_contents = file_manager.read()
	file_manager.close()
	#change to the "right module name"
	file_contents= file_contents.replace(old_module_name,new_module_name)
	#write changes
	file_manager=open(file_path,'w')
	file_manager.write(file_contents)
	file_manager.close()

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

import os
import subprocess
from compile_support_module import *
from finding_regexes import *
import re
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

def get_input_file(root):
	return re.search('\d+\_\d', root).group(0)


def run_python_2x(file_path,path_input,c_id,root):
	errors = run_python_commando('python ',file_path,path_input)
	if len(errors) > 0:
		error_list = filter_information('\w+Error',None,errors)
		if len(error_list)>0:
			error_name = error_list[0]
			if error_name =='ImportError':
				handle_import_error(file_path,path_input,errors,'pip')
				return run_python_2x(file_path,path_input,c_id,root)
			elif error_name == 'SyntaxError':
				return run_python_3x(file_path,path_input,c_id,root)
			elif error_name =='FileNotFoundError' or error_name == 'IOError':
				handle_file_not_found(path_input,root,c_id,file_path)
				return run_python_2x(file_path,path_input,c_id,root)
		print errors
		return 0
	return 1


def handle_file_not_found(input_file,root,c_id,file_path):
	file_contents,file_manager = get_contents_of_file(file_path)
	changed_content = rename_input_file(file_contents,input_file)
	write_new_contents_to_the_file(file_path,changed_content) # write changes to the python file
	file_contents,file_manager = get_contents_of_file(file_path)
	changed_contents = rename_output_file(file_contents,root)
	write_new_contents_to_the_file(file_path,changed_contents)



def create_a_copy_of_input_file(c_id,input_file):
	dst = input_file + '(1)'
	number_of_files = len(os.listdir(PATH_INPUT+c_id)) 
	copyfile(input_file, dst) #create a copy of input file
	return dst,number_of_files

def rename_input_file(file_contents,input_file):
	old_regex = find_out_what_regex('open\((.*[\'\"]r[\'\"])\)',file_contents) # find out what regex
	new_regex = 'open (\'' + input_file + '\''+ ',' +' \'r\')'
	if old_regex is None:
		old_regex = find_out_what_regex('with open\((.*?)\)',file_contents)
		new_regex = 'with open (\'' + input_file + '\''+ ',' +' \'r\')' 
		if old_regex is None :
			old_regex = find_out_what_regex('file\(.*?\)',file_contents)
			new_regex = 'file(' + input_file +')'
	print 'OLD REGEX ' + old_regex
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

def handle_import_error(file_path,path_input,errors,pip_version):
	missing_module_name = filter_information('named\s\w+',None,errors)[0]
	missing_module_name = missing_module_name.replace('named','')
	if missing_module_name == 'run':
		rename_stuff_in_file('runpy','run',file_path,1)
	else :
		pip_errors = pip_install_module(pip_version,missing_module_name)
		if len(pip_errors)>0: # No module found
			rename_stuff_in_file('','import ' + missing_module_name,file_path) #try to remove module
	return 1


def run_python_3x(file_path,path_input,c_id,root):
	errors = run_python_commando('python3 ',file_path,path_input)
	if len(errors) > 0:
		error_list = filter_information('\w+Error',None,errors)
		print error_list
		if len(error_list)>0:
			error_name = error_list[0]			
			if error_name =='ImportError':
				handle_import_error(file_path,path_input,errors,'pip3')
				return run_python_3x(file_path,path_input,c_id,root)
			elif error_name == ('FileNotFoundError' or 'IOError'):
				handle_file_not_found(path_input,root,c_id,file_path)
				return run_python_3x(file_path,path_input,c_id,root)
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





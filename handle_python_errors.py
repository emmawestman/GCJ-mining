from compile_support_module import *
import subprocess
from shutil import copyfile
from handle_compilation_errors import *
from finding_regexes import *



def handle_import_error(file_path,path_input,errors,pip_version):
	missing_module_name = find_missing_module_name(errors)
	if '\'' in missing_module_name :
		missing_module_name = missing_module_name[1:len(missing_module_name)-1]
	print 'handle import error ' + missing_module_name
	if missing_module_name == 'run':
		rename_stuff_in_file('runpy','run',file_path,1)
	else :
		pip_errors = pip_install_module(pip_version,missing_module_name)
		if len(pip_errors)>0:
			print pip_errors
			return 0,missing_module_name
	return 1,None


def handle_python_file_not_found(input_file,root,c_id,file_path):
	new_input = '\''+input_file+'\'' + ' ,\'r\''
	new_output = '\''+os.path.join(root,'output.txt') + '\' ,\'w\''
	list_of_inregexes = get_possible_input_regex()
	list_of_outregexes = get_possible_output_regex()
	handle_file_not_found(file_path,list_of_inregexes,list_of_outregexes,new_input,new_output)


def get_error_name (errors):
	error_list = filter_information('\w+Error',None,errors)
	if len(error_list)>0:
		error_name = error_list[0]
		return error_name
	return errors 

def pip_install_module(pip_version,module_name):
	cmd = [pip_version + ' install ' + module_name]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors


def create_a_copy_of_input_file(c_id,input_file):
	dst = input_file + '(1)'
	number_of_files = len(os.listdir(PATH_INPUT+c_id)) 
	copyfile(input_file, dst) #create a copy of input file
	return dst,number_of_files

#dictionary for old- new regex pairs
def get_possible_input_regex():
	return ['open\([\"\'](?:[\w]\:)?(?:/\w+)+?(?:\w+).\w+(?:[\'\"]),[\'\"]r[\'\"]\)','open\(.*[\'\"]r[\'\"]\)','with open\(.*?[\'\"]?r?[\'\"]?\) as \w+\s?[,:]','file\(.*?\)','open\(.*[\'\"]?r?[\'\"]?\)']

def get_possible_output_regex():
	return ['open\([\"\'](?:[\w]\:)?(?:/\w+)+.\w+(?:[\'\"]),[\'\"][aw][\'\"]\)','open\(.*?[\'\"]w[\'\"]\)','with open\(.*?[\'\"][wa][\'\"]\)']


#TODO FIXA
def remove_copy_of_input_file(number_of_files,dst,root,c_id):
	return 0

#TODO FIXA DETTA
def find_missing_module_name(errors):
	missing_module_name = find_out_what_regex('named\s(\'?\w+\'?)',errors)
	missing_module_name = missing_module_name[0].replace('named ','')
	if missing_module_name is len(missing_module_name) == 0  :
		missing_module_name = find_out_what_regex('from\s(\w+)\simport',errors)
		missing_module_name = missing_module_name.replace('from ','')
		missing_module_name = missing_module_name.replace(' import','')
	return missing_module_name




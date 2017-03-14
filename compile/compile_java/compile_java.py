import os
import subprocess
import sys

# import own modules from diffrent directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *
gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from finding_regexes import *
from constants import *

def file_not_found_exception(errors,class_name,user_path,old_problem_name,p_id):
	requested_file_name =filter_information(':\s.*\.\w*',':',errors)[0]
	requested_file_name = requested_file_name.replace(':','')
	PATH_INPUT = os.path.join(os.getcwd(), '../../../../../../input_' + p_id)
	rename_file(user_path,PATH_INPUT,old_problem_name,requested_file_name)
	os.chdir(user_path)
	return run_java_command(class_name,requested_file_name)


def run_java_file(user_path,problem_folder,user_folder,class_name, p_id):
	print 'running java file ' + problem_folder + ' ' + user_folder + ' ' + class_name 
	PATH_INPUT = os.path.join(os.getcwd(), '../../../../../../input_' + p_id)
	user, input_file = get_run_info('java', os.getcwd())
	path_to_input = os.path.join(PATH_INPUT, input_file)
	args = '< '+ path_to_input

	flag,errors = run_java_command(class_name, args)
	if flag == 0 and errors != None:
		exception_name = get_exception_name(errors)
		if exception_name == 'FileNotFoundException':
			flag,errors = file_not_found_exception(errors,class_name,user_path,input_file, p_id)
			print errors
			return flag
		return 0
	return 1


def run_java_command(class_name,args):	
	cmd = ['timeout 30s java ' + class_name + ' ' + args ]
	exit_code, errors = full_exe_cmd(cmd)
	if exit_code == 0:
		if errors.find('Exception in thread')!= -1:
			return 0,errors
		return 1,None
	else:
		return 0, None

def getUser
	

def compile_java(p_id, dict):
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + p_id, 'java' ))
	nbr_of_files = 0
	succes_nbr = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			if (f.endswith(".java")):
				full_path = os.path.join(root,f)
				exit_code, errors = run_process_compile(full_path)
				dict = set_compiler_to_none(dict,full_path)
				if int(exit_code) == 0:
					if 'Note' in errors or len(errors) == 0:
						succes_nbr += 1
						user_dict['compiled'] = 'YES'
					else:
						print errors
						user_dict['compiled'] = 'NO'
				else :
					print 'Timeout for file: ' + full_path
					user_dict['compiled'] = 'NO'
	print dict
	return succes_nbr, nbr_of_files, dict

def run_process_compile(full_path) :
	cmd = ['timeout 30s javac ' + full_path]
	return run_process(cmd)

def set_compiler_to_none(dict,full_path) :
	user_id = get_user_id(full_path)
	user_dict = dict[user_id]
	user_dict['compiler_version'] = '-'
	return dict


def run_java_files(p_id) :
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + p_id, 'java'))
	nbr_of_files = 0
	succes_nbr = 0
	#List problemfolders
	problemfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
	
	for problem_folder in problemfolders:
		problemPATH = os.path.join(path, problem_folder)
		#List userfolders
		userfolders = [f for f in os.listdir(problemPATH) if os.path.isdir(os.path.join(problemPATH, f))]
		for user_folder in userfolders:
			nbr_of_files += 1
			userPATH = os.path.join(problemPATH,user_folder)
			os.chdir(userPATH)
			#Filter class name
			java_file = [f for f in os.listdir(userPATH) if f.endswith('.java')][0] #TODO: ASSUMES THAT ONLY EXIST ONE JAVA FILE
			class_file =[ f for f in os.listdir(userPATH) if (f.endswith(".class") and f.split('.')[0])==java_file.split('.')[0] ] #TODO : FULT MEN WHAT TO DO
			
			if len(class_file)>0:
					class_name = class_file[0].split('.')[0]
					succes_nbr += run_java_file(userPATH,problem_folder,user_folder,class_name, p_id)
	return succes_nbr, nbr_of_files


def get_exception_name(errors):
	return  re.search('java.\w*.\w*', errors).group().split('.')[2]

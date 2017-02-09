import os
import subprocess
from compile_support_module import *
from finding_regexes import *


def file_not_found_exception(errors,class_name,user_path,old_problem_name):
	requested_file_name =filter_information(':\s.*\.\w*',':',errors)[0]
	requested_file_name = requested_file_name.replace(':','')
	rename_file(user_path,PATH_INPUT,old_problem_name,requested_file_name)
	os.chdir(user_path)
	print run_java_command(class_name,requested_file_name)

def run_java_file(user_path,problem_folder,user_folder,class_name):
	print 'running java file ' + problem_folder + ' ' + user_folder + ' ' + class_name 
	old_problem_name = get_input_file(problem_folder) 
	path_to_input = os.path.join(PATH_INPUT,old_problem_name)
	args = '< '+ path_to_input
	errors = run_java_command(class_name, args)
	if errors is not None:
		exception_name = get_exception_name(errors)
		if exception_name == 'FileNotFoundException':
			file_not_found_exception(errors,class_name,user_path,old_problem_name)
			return 1
		else:
			errors
			return 0
	return 1


def run_java_command(class_name,args):	
	cmd = ['java ' + class_name + ' ' + args ]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output, errors = p.communicate()
	if errors.find('Exception in thread')!= -1:
		return errors


def compile_java(path):
	nbr_of_files = 0
	succes_nbr = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			if (f.endswith(".java")):
				try:
					subprocess.check_call(['javac', os.path.join(root,f) ])
				except subprocess.CallProcessError:
					pass
				succes_nbr += 1
	return succes_nbr, nbr_of_files

def run_java_files(path) :
	nbr_of_files = 0
	succes_nbr = 0
	problemfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
	for problem_folder in problemfolders:
		problemPATH = os.path.join(path, problem_folder)
		userfolders = [f for f in os.listdir(problemPATH) if os.path.isdir(os.path.join(problemPATH, f))]
		for user_folder in userfolders:
			nbr_of_files += 1
			userPATH = os.path.join(problemPATH,user_folder)
			os.chdir(userPATH)
			java_file = [f for f in os.listdir(userPATH) if f.endswith('.java')][0] #TODO: ASSUMES THAT ONLY EXIST ONE JAVA FILE
			class_file =[ f for f in os.listdir(userPATH) if (f.endswith(".class") and f.split('.')[0])==java_file.split('.')[0] ] #TODO : FULT MEN WHAT TO DO
			if len(class_file)>0:
					class_name = class_file[0].split('.')[0]
					succes_nbr += run_java_file(userPATH,problem_folder,user_folder,class_name)
	return succes_nbr, nbr_of_files



def get_exception_name(errors):
	return  re.search('java.\w*.\w*', errors).group().split('.')[2]

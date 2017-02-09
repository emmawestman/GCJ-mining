import os
import subprocess
from compile_support_module import *

def file_not_found_exception(errors,class_name,user_path,old_problem_name):
	indexes =filter_substring(':',' (No',errors)
	new_file_name = errors[indexes[0]+2:indexes[1]]
	rename_file(user_path,PATH_INPUT,old_problem_name,new_file_name)
	os.chdir(user_path)
	print run_java_command(class_name,new_file_name)

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
		else:
			print 'JAVA EXCEPTION ' + exception_name


def run_java_command(class_name,args):	
	cmd = ['java ' + class_name + ' ' + args ]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output, errors = p.communicate()
	if errors.find('Exception in thread')!= -1:
		return errors

def compile_java(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			if (f.endswith(".java")):
				subprocess.check_call(['javac', os.path.join(root,f) ])


def run_java_files(path) :
	problemfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
	for problem_folder in problemfolders:
		problemPATH = os.path.join(path, problem_folder)
		userfolders = [f for f in os.listdir(problemPATH) if os.path.isdir(os.path.join(problemPATH, f))]
		for user_folder in userfolders:
			userPATH = os.path.join(problemPATH,user_folder)
			os.chdir(userPATH)
			java_file = [f for f in os.listdir(userPATH) if f.endswith('.java')][0] #TODO: ASSUMES THAT ONLY EXIST ONE JAVA FILE
			class_file =[ f for f in os.listdir(userPATH) if (f.endswith(".class") and f.split('.')[0])==java_file.split('.')[0] ] #TODO : FULT MEN WHAT TO DO
			if len(class_file)>0:
					class_name = class_file[0].split('.')[0]
					run_java_file(userPATH,problem_folder,user_folder,class_name)


def get_exception_name(errors):
	indexes = filter_substring('java.+\n','.',errors)
	exception_name = errors[indexes[0]:indexes[1]].split('.')[2]
	return exception_name

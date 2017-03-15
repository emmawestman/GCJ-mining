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

def run_java_file(root,class_name,dict,p_id):
	print 'running java file ' + root
	error_code, errors = run_java_command(build_run_args(root,class_name,p_id))
	#write statistics to cvs
	dict = set_run_mesurments(exit_code, errors, dict, root)
	if int error_code != 0:
		print errors
	return dict
		
def build_run_args(root,class_name,p_id):
	path_to_input = os.path.join(get_HOME_PATH(), '/datacollection/input', p_id)
	args = '< '+ path_to_input
	return root +' '+class_name + ' ' + args 

def run_java_command(args):	
	cmd = 'timeout 30s java -classpath ' + args
	return full_exe_cmd(cmd)	

def compile_java_command(full_path):
	cmd = 'timeout 30s javac ' + full_path
	return run_process(cmd) 

def compile_java(p_id, dict):
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + p_id, 'java' ))
	for root, dirs, files in os.walk(path):
		for f in files:
			if (f.endswith(".java")):
				full_path = os.path.join(root,f)
				exit_code, errors = run_process_compile(full_path)
				# write compile statistics
				dict = set_compiler_version(dict,full_path,'-')
				dict = set_compile_exitcode(dict,full_path,exit_code)  				
	return dict


def run_java_files(p_id,dict) :
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + p_id, 'java'))
	for root, dirs, files in os.walk(path):
		for f in files :
			if f.endswith(".class"):
				class_name = class_file[0].split('.')[0]
				dict = run_java_file(root,class_name,dict,p_id)
	return dict


def get_exception_name(errors):
	return  re.search('java.\w*.\w*', errors).group().split('.')[2]

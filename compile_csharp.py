
import os
import subprocess
import re
from stuff_module import create_folder
from compile_support_module import *
from finding_regexes import *


def compile_run_csharp(c_id):
	path = os.path.realpath(os.path.join('..','solutions_' + c_id, 'C#' ))
	PATH_INPUT = os.path.realpath(os.path.join('..','input_' + c_id))
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith('.cs'):
				nbr_of_files += 1
				print 'Compiling problem: ' + filename + ', for user: ' + user
				filename = get_input_file(root)+'.in'
				input_file = os.path.join(input_path,filename)
				succes_nbr += compile_csharp (root,f,None,input_file,None) # REALLY COMPILE AND RUN CSHARP
	return succes_nbr, nbr_of_files


def build_arguments (flag,csharp_file,csharp_file_p_dependecy,root):
	csharp_file = ''
	if flag is not None:
		csharp_file = '-r:'+flag+'.dll '
	csharp_file+= os.path.join(root,csharp_file_p)
	if csharp_file_p_dependecy is not None :
		csharp_file = csharp_file + ' ' + os.path.join(root,csharp_file_p_dependecy)
	return csharp_file

def compile_and_run_csharp(root,csharp_file_p,csharp_file_p_dependecy,input_file,flag):
	csharp_file = build_arguments (flag,csharp_file,csharp_file_p_dependecy,root)
	errors = compile_csharp_command(csharp_file)
	if len(errors)>0:
		handle_compilation_errors(errors)
		return 0
	csharp_= csharp_file_p.replace('.cs','.exe')
	if csharp_file_p_dependecy is not None:
		csharp_file_p = csharp_file_p_dependecy
		return run_csharp(input_file,root,os.path.join(root,csharp_exe),csharp_file_p)

def compile_csharp_command(csharp_file):
	cmd = ['timeout 30s mcs ' + csharp_file]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors


def run_csharp_command(csharp_exe,input_file):
	if input_file is not None :
		csharp_exe = csharp_exe + ' < ' + input_file
	cmd = ['timeout 30s mono ' + csharp_exe ]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors


def run_csharp(input_file,root,csharp_exe,original_class_file):
	errors = run_csharp_command(csharp_exe,input_file)
	if len(errors)>0:
		handle_run_errors(errors)
	return 1


def handle_compilation_errors(errors):
	if "does not contain a static `Main' method suitable for an entry point" in errors:
		create_main_file()
		return compile_csharp (root,'TestMain.cs',csharp_file_p,input_file,flag)
	if 'The type or namespace name' in errors:
		old_regex = filter_information('\`\w+\'',None,errors)[0]
		old_regex = old_regex.replace('`','')
		old_regex = old_regex.replace ('\'','')
		new_regex = filter_information('\`\w+[.]\w+\'',None,errors)
		if len(new_regex)>0 :
			new_regex = new_regex[0]
			new_regex = new_regex.replace('`','')
			new_regex = new_regex.replace ('\'','')
			return compile_csharp (root,csharp_file_p,csharp_file_p_dependecy,input_file,new_regex)
	print errors
	return 0

def handle_run_errors(errors):
	error_name = filter_information('Unhandled Exception:\n\w+\.\w+\.\w+',':',errors)
	if error_name and error_name[0].replace('\n','') == ('System.IO.DirectoryNotFoundException' or 'System.IO.FileNotFoundException') and input_file is not None:
		remove_files_in_a_user_solution(root)
		change_input_streams(input_file,os.path.join(root,original_class_file),root)
		return compile_csharp(root,original_class_file,None,None,None)
	print errors
	return 0


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


def remove_files_in_a_user_solution(root):
	files = os.listdir(root)
	filelist = [ f for f in files if (f == 'TestMain.cs' or f.endswith('.exe')) ]
	for file in filelist:			
		os.remove(os.path.join(root,file))

def compile_csharp(root,csharp_file_p,csharp_file_p_dependecy,input_file,flag):
	csharp_file = ''
	if flag is not None:
		csharp_file = '-r:'+flag+'.dll '
	csharp_file+= os.path.join(root,csharp_file_p)
	if csharp_file_p_dependecy is not None :
		csharp_file = csharp_file + ' ' + os.path.join(root,csharp_file_p_dependecy)
	print 'CSHARP COMMAND ' + csharp_file
	errors = compile_csharp_command(csharp_file)
	if len(errors)>0:
		print errors
		if "does not contain a static `Main' method suitable for an entry point" in errors:  #TODO make a method for errors
			# find function in file to call from main
			# find namespace
			namespace = find_namespace(csharp_file_p, root)
			# create main file and call some function...
			filter_candidates = filter_candidate_functions(os.path.join(root,csharp_file_p))
			csharp_main(filter_candidates[0], csharp_file_p, namespace, root,input_file)
			# run main file instead
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
	else :
		csharp_= csharp_file_p.split('.')[0]
		csharp_exe = csharp_ + '.exe'
		print 'CSHARP FILE ' + csharp_exe
		if csharp_file_p_dependecy is not None:
			csharp_file_p = csharp_file_p_dependecy
		return run_csharp(input_file,root,os.path.join(root,csharp_exe),csharp_file_p)

def compile_csharp_command(csharp_file):
	cmd = ['mcs ' + csharp_file]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

def run_csharp(input_file,root,csharp_exe,original_class_file):
	errors = run_csharp_command(csharp_exe,input_file)
	if len(errors)>0:
		error_name = filter_information('Unhandled Exception:\n\w+\.\w+\.\w+',':',errors)
		if error_name and error_name[0].replace('\n','') == ('System.IO.DirectoryNotFoundException' or 'System.IO.FileNotFoundException') and input_file is not None:
			remove_files_in_a_user_solution(root)
			change_input_streams(input_file,os.path.join(root,original_class_file),root)
			return compile_csharp(root,original_class_file,None,None,None)
		print errors
		return 0
	return 1

def run_csharp_command(csharp_exe,input_file):
	if input_file is not None :
		csharp_exe = csharp_exe + ' < ' + input_file
	cmd = ['mono ' + csharp_exe ]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors


def change_input_streams(input_file,csharp_file,root):
	file_contents = get_contents_of_file(file_path)
	file_contents = rename_input_file('new StreamReader\((.*)\)','\"'+input_file+'\"',input_file,file_contents)
	new_output = '\"' + os.path.join(root,'output.txt') + '\"'
	file_contents = rename_output_file('new StreamWriter\((.*)\)',new_output,file_contents,root)
	write_new_contents_to_the_file(csharp_file,file_contents)

def csharp_main(full_function_decl, filename, namespace, path,input_file):
	index = len(filename) -3
	filename = filename[:index]
	function_name = re.findall(r'(\w+)',full_function_decl)[0]
	main_file= os.path.join(path, 'TestMain.cs')         
	file1 = open(main_file, "w")
	file_content = 'namespace ' + namespace + '\n' + '{ \n class TestMain \n { \n static void Main() \n { \n' + filename + '.' + function_name + build_main_function(full_function_decl,input_file) + ' \n } \n } \n }'
	file1.write(file_content)
	file1.close()

#ONLY CHOOSING STATIC FUNCTIONS
def filter_candidate_functions(file_path):
	file_manager = open(file_path,'r')
	file_contents = file_manager.read()
	list_of_stuff = []
	p = re.compile('static\s(?:int|void|long|string)\s(\w+\([\w+\s]*?\))')
	return p.findall(file_contents)

#ONLY HANDLING ONE StreamWriter and StreamReader
def build_main_function(filtered_function,input_file):
	main_string = '('
	p = re.compile('(\w+\s\w+)')
	list_of_args = p.findall(filtered_function) 
	for x in range(0,len(list_of_args)) :
		group = list_of_args[x]
		arg_type = group.split(' ')[0]
		arg_decl = ''
		if arg_type == 'StreamReader':
			arg_decl = 'new StreamReader(\''+ input_file + '\')'
		if arg_type == 'StreamWriter':
			arg_decl = 'new StreamWriter(output.txt)'
		main_string+= arg_decl
		if x != len(list_of_args)-1 and ',' in main_string:
			main_string+= ','
	main_string+=');'
	return main_string

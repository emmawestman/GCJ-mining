
import os
import shutil
import subprocess
from stuff_module import create_folder
from compile_support_module import *
from finding_regexes import *


def compile_run_csharp(c_id):
	path = os.path.realpath(os.path.join('..','solutions_' + c_id, 'C#' ))
	PATH_INPUT = os.path.realpath(os.path.join('..','input_' + c_id))
	#number of files that successfylly compiles
	remove_old_files('.cs',path)
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith('.cs'):
				nbr_of_files += 1
				regexp = "/C#/"
				index = root.find(regexp)
				filename = root[index+len(regexp):]
				index = filename.find('/')
				user = filename[index+1:]
				filename = filename[:index]
				print 'Compiling problem: ' + filename + ', for user: ' + user
				filename = filename + '.in'
				input_file = os.path.join(PATH_INPUT,filename)
				succes_nbr = compile_csharp (root,f,None,input_file) # REALLY COMPILE AND RUN CSHARP
	return succes_nbr, nbr_of_files


def compile_csharp(root,csharp_file_p,csharp_file_p_dependecy,input_file):
	csharp_file = os.path.join(root,csharp_file_p)
	if csharp_file_p_dependecy is not None :
		csharp_file = csharp_file + ' ' + os.path.join(root,csharp_file_p_dependecy)
	errors = compile_csharp_command(csharp_file)
	if len(errors)>0:
		if "does not contain a static `Main' method suitable for an entry point" in errors:
			# find function in file to call from main
			# find namespace
			namespace = find_namespace(csharp_file_p, root)
			# create main file and call some function...
			csharp_main('SolveProblem', csharp_file_p, namespace, root)
			# run main file instead
			return compile_csharp (root,'TestMain.cs',csharp_file_p,input_file)
		else:
			print errors

			if len(errors) > 0:
				# fix issue where no main is missing
				print "ERRORRR " + errors
				if "does not contain a static `Main' method suitable for an entry point" in errors:
					# find function in file to call from main
					# find namespace
					namespace = find_namespace(f, root)
					# create main file and call some function...
					csharp_main('SolveProblem', f, namespace, root)
					# run main file instead
					cmd = ['mcs ' + os.path.join(root,'TestMain.cs ') + os.path.join(root, f)]# + ' < ' + os.path.join(PATH_INPUT,filename)]
					p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					output, errors = p.communicate()
					if len(errors) > 0 :
						print 'I give up'
						print errors
					else: 
						succes_nbr += 1
						#print 'Successfully added and compiled main!' 
						# run main file
						cmd = ['mono ' + os.path.join(root,'TestMain.exe ')]# + ' < ' + os.path.join(PATH_INPUT,filename)]
						p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						output, errors = p.communicate()
						# gives "wrong" error message, not the same as when run manually
						print errors
						if len(errors) > 0:
							
							#rename input file... hard when error message not displayed
							# this is a hard coded test case
							# --create folder GCJ
							
							create_folder(os.path.join(root, "D:\\GCJ" ))
							create_folder(os.path.join(root,"D:\\GCJ", 'sheep'))
							input_path = os.path.join(PATH_INPUT, filename)
							in_file = open(input_path, 'r')
							content = in_file.read()
							in_file.close()
							new_file = os.path.join(root, "D:\\GCJ"	, 'sheep', 'input.txt')
							out_file = open(new_file, 'w')
							out_file.write(content)
							out_file.close()
							#rename_file(root, PATH_INPUT, filename, 'input.txt')
							# run again
							cmd = ['mcs ' + os.path.join(root,'TestMain.exe ') + ' < ' + new_file]
							p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
							output, errors = p.communicate()

			return 0
	else :
		csharp_= csharp_file_p.split('.')[0]
		csharp_exe = csharp_ + '.exe'
		print 'CSHARP FILE ' + csharp_exe
		return run_csharp(input_file,os.path.join(root,csharp_exe))

def compile_csharp_command(csharp_file):
	cmd = ['mcs ' + csharp_file]
	print cmd
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

def run_csharp(input_file,csharp_exe):
	errors = run_csharp_command(csharp_exe)
	if len(errors)>0:
		error_name = filter_information('Unhandled Exception:\n\w+\.\w+\.\w+',':',errors)
		if error_name == 'System.IO.DirectoryNotFoundException':
			rename_input_file(input_file,csharp_file)
			return run_csharp(csharp_file)
		else :
			print errors
			return 0
	return 1

def run_csharp_command(csharp_exe):
	cmd = ['mono ' + csharp_exe]# + ' < ' + os.path.join(PATH_INPUT,filename)]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

def rename_input_file(input_file,csharp_file):
	old_regex = 'StreamReader\(.+\);'
	new_regex = 'StreamReader('+ input_file + ');'
	rename_stuff_in_file(new_regex,old_regex,csharp_file)

def csharp_main(function_name, filename, namespace, path):
	index = len(filename) -3
	filename = filename[:index]
	main_file= os.path.join(path, 'TestMain.cs')         
	file1 = open(main_file, "w")
	file_content = 'namespace ' + namespace + '\n' + '{ \n class TestMain \n { \n static void Main() \n { \n' + filename + '.' + function_name + '();' + ' \n } \n } \n }'
	file1.write(file_content)
	file1.close()

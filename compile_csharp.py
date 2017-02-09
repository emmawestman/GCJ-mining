
import os
import shutil
import subprocess
from stuff_module import create_folder
from compile_support_module import find_namespace

PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016'))
PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))

def compile_run_csharp(path):
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			regexp = "/C#/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			filename = filename[:index]
			print 'Compiling problem: ' + filename + ', for user: ' + user
			filename = filename + '.in'
			
			cmd = ['mcs ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				# fix issue where no main is missing
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
						print 'Successfully added and compiled main!' 
						# run main file
						cmd = ['mcs ' + os.path.join(root,'TestMain.exe ')]# + ' < ' + os.path.join(PATH_INPUT,filename)]
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

			else:
				succes_nbr += 1
				print 'Successfully compiled!'
				# run file
				cmd = ['mono ' + os.path.join(root, f+'.exe ')]# + ' < ' + os.path.join(PATH_INPUT,filename)]
				print cmd
				p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output, errors = p.communicate()
				print errors
	return succes_nbr, nbr_of_files

def csharp_main(function_name, filename, namespace, path):
	index = len(filename) -3
	filename = filename[:index]
	main_file= os.path.join(path, 'TestMain.cs')         
	file1 = open(main_file, "w")
	file_content = 'namespace ' + namespace + '\n' + '{ \n class TestMain \n { \n static void Main() \n { \n' + filename + '.' + function_name + '();' + ' \n } \n } \n }'
	file1.write(file_content)
	file1.close()

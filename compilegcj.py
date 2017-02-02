import os
import shutil
from stuff_module import create_folder
from compile_java import *
from compile_python import *
PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016'))
PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))



def compile_run_csharp(path):
	for root, dirs, files in os.walk(path):
		for f in files:
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
						print 'Successfully added and compiled main!' 
						# run main file
						cmd = ['mcs ' + os.path.join(root,'TestMain.exe ')]# + ' < ' + os.path.join(PATH_INPUT,filename)]
						p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						output, errors = p.communicate()
						# gives "wrong" error message, not the same as when run manually
						print errors
						if len(errors) > 0:
							#rename input file... hard when error message cant be parsed
							# this is a hard coded test
							# --create folder GCJ
							rename_file(root, PATH_INPUT, filename, 'sheep/input.txt')

			else:
				print 'Successfully compiled!'
				# run file
				cmd = ['mono ' + os.path.join(root, f+'.exe ')]# + ' < ' + os.path.join(PATH_INPUT,filename)]
				print cmd
				p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output, errors = p.communicate()
				print errors

def csharp_main(function_name, filename, namespace, path):
	index = len(filename) -3
	filename = filename[:index]
	main_file= os.path.join(path, 'TestMain.cs')         
	file1 = open(main_file, "w")
	file_content = 'namespace ' + namespace + '\n' + '{ \n class TestMain \n { \n static void Main() \n { \n' + filename + '.' + function_name + '();' + ' \n } \n } \n }'
	file1.write(file_content)
	file1.close()


def compile_language(language):
	path = os.path.join(PATH, language)
	if language == 'java':
		java_path = build_language_path(language)
		remove_class_files(language,java_path)
		compile_java(java_path)
		run_java_files(java_path)
	elif language == 'C':
		print "C has no compile script yet"
		print 'inne i c'
	elif language == "C++":
		print "C++ has no compile script yet"
	elif language == 'C#':
		csharp_path = build_language_path('C#')
		compile_run_csharp(csharp_path)
	elif language == "Python":
		python_path = build_language_path('Python')
		compile_python(python_path)
	else: 	
		print language ++ " is not one of the selected languages, try: java, C, C++, C# or Python"


compile_language("Python")






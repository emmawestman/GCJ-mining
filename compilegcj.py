import os
import subprocess
import shutil
from stuff_module import create_folder

PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016'))
PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))

def build_language_path(language):
	new_path = os.path.join(PATH,language)
	return new_path

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

def filter_substring(error_message_start,error_message_end,error_string):
	indexes = []
	start_index =error_string.find(error_message_start)
	end_index = error_string.find(error_message_end)
	indexes.append(start_index)
	indexes.append(end_index)
	return indexes

def get_exception_name(errors):
	indexes = filter_substring('java.',':',errors)
	exception_name = errors[indexes[0]:indexes[1]].split('.')[-1]
	return exception_name

def get_input_file(problem_folder):
	problem_input = [f for f in os.listdir(PATH_INPUT) if (f.split('.')[0]==problem_folder)]
	return problem_input[0]

def run_java_command(class_name,args):	
	cmd = ['java ' + class_name + ' ' + args ]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output, errors = p.communicate()
	return errors

	
def file_not_found_exception(errors,class_name,user_path,old_problem_name):
	indexes =filter_substring(':',' (',errors)
	new_file_name = errors[indexes[0]+2:indexes[1]]
	print 'FILE NAME' + new_file_name
	rename_file(user_path,PATH_INPUT,old_problem_name,new_file_name)
	os.chdir(user_path)
	print run_java_command(class_name,new_file_name)

def run_java_file(user_path,problem_folder,user_folder,class_name):
	print 'running java file ' + problem_folder + ' ' + user_folder + ' ' + class_name 
	old_problem_name = get_input_file(problem_folder) 
	path_to_input = os.path.join(PATH_INPUT,old_problem_name)
	args = '< '+ path_to_input
	errors = run_java_command(class_name, args)
	if len(errors)>0 :
		exception_name = get_exception_name(errors)
		if exception_name == 'FileNotFoundException':
			file_not_found_exception(errors,class_name,user_path,old_problem_name)
		else:
			print 'JAVA EXCEPTION ' + exception_name
		

def rename_file(user_path,path_to_file,old_file_name,new_file_name):
	dest_path= user_path
	if new_file_name.find('/') !=-1:
		path_to_create_folder = new_file_name.split('/')
		curr_path = user_path
		new_file_name = path_to_create_folder[-1]
		lim = len(path_to_create_folder)-1
		for x in range(0,lim):
			name = path_to_create_folder[0]
			create_folder(name)
			curr_path = os.path.join(curr_path,name) 
			os.chdir(curr_path)
		shutil.copy(os.path.join(path_to_file,old_file_name),curr_path)
		os.rename(old_file_name,new_file_name)
	else:
		shutil.copy(os.path.join(path_to_file,old_file_name),dest_path)
		os.rename(old_file_name,new_file_name)
		
								

def compile_python(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			regexp = "/Python/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			filename = filename[:index]
			print 'Running problem: ' + filename + ', for user: ' + user
			filename = filename + '.in'
			
			cmd = ['python ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				print 'error'
			else:
				print 'Successfully compiled!'

	
			
		
			'''if errors.startswith('Traceback'):
				print error
			else:
				print 'Successfully copiled and ran ' + os.path.join(root,f)'''

def compile_csharp(path):
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
					cmd = ['mcs ' + os.path.join(root,'TestMain.cs ') + os.path.join(root, f) + ' < ' + os.path.join(PATH_INPUT,filename)]
					p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					output, errors = p.communicate()
					if len(errors) > 0 :
						print 'I give up'
						print errors
					else: 
						print 'Successfully added and ran main!' 
			else:
				print 'Successfully compiled!'

def csharp_main(function_name, filename, namespace, path):
	index = len(filename) -3
	filename = filename[:index]
	main_file= os.path.join(path, 'TestMain.cs')         
	file1 = open(main_file, "w")
	file_content = 'namespace ' + namespace + '\n' + '{ \n class TestMain \n { \n static void Main() \n { \n' + filename + '.' + function_name + '();' + ' \n } \n } \n }'
	file1.write(file_content)
	file1.close()

def find_namespace(filename, path):
	full_path = os.path.join(path, filename)
	file1 = open(full_path, "r")
	content = file1.read()
	index_start = content.find('namespace ') + len('namespace ')
	content = content[index_start:]
	index_end = content.find('\n')
	namespace = content[:index_end]
	return namespace





def remove_class_files(language_path):
	for root, dirs, files in os.walk(language_path):
		filelist = [ f for f in files if not(f.endswith(".java")) ]
		for f in filelist:			
			os.remove(os.path.join(root,f))


#remove_class_files()		
#compile_java()
#run_java_files(build_language_path('java'))



def compile_language(language):
	path = os.path.join(PATH, language)
	if language == 'java':
		java_path = build_language_path('java')
		remove_class_files(path)
		compile_java(java_path)
		run_java_files(java_path)
	elif language == 'C':
		print "C has no compile script yet"
		print 'inne i c'
	elif language == "C++":
		print "C++ has no compile script yet"
	elif language == 'C#':
		csharp_path = build_language_path('C#')
		compile_csharp(csharp_path)
	elif language == "Python":
		python_path = build_language_path('Python')
		compile_python(python_path)
	else: 	
		print language ++ " is not one of the selected languages, try: java, C, C++, C# or Python"


<<<<<<< HEAD
#compile_language("Python")
compile_language("C#")



#remove_class_files()
#compile_language('java')
#folder_name = build_language_path('java')
#run_java_files(folder_name)
=======

#compile_language("Python")

>>>>>>> 9e76627355f3fac95c4a11822791c8e08c9ce4ea


#folder_name = build_language_path('java')
#remove_class_files(folder_name)
compile_language('java')
#run_java_files(folder_name)
#remove_class_files()
#compile_language("Python")
#compile_python()




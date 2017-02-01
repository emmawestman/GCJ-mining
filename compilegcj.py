import os
import subprocess


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
			try:
				java_file = [f for f in os.listdir(userPATH) if f.endswith('.java')][0] #TODO: ASSUMES THAT ONLY EXIST ONE JAVA FILE
				class_file =[ f for f in os.listdir(userPATH) if (f.endswith(".class") and f.split('.')[0])==java_file.split('.')[0] ] #TODO : FULT MEN WHAT TO DO
				if len(class_file)>0:
					class_name = class_file[0].split('.')[0]
					run_java_file(problem_folder,user_folder,class_name)
			except IndexError,e :
				print 'This folder doesnt have a java file ' + problem_folder + ' ' + user_folder


def run_java_file(problem_folder,user_folder,class_name):
	print 'running java file ' + problem_folder + ' ' + user_folder + ' ' + class_name 
	cmd = ['java ' +class_name]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output, errors = p.communicate()
	print output

		
								

def compile_python(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			regexp = "/Python/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			filename = filename[:index] + '.in'
			#print  os.path.join(PATH_INPUT,filename)
		
			cmd = ['python ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			output, errors = p.communicate()



def remove_class_files(language_path):
	for root, dirs, files in os.walk(language_path):
		filelist = [ f for f in files if not(f.endswith(".java")) ]
		for f in filelist:			
			os.remove(os.path.join(root,f))

def compile_language(language):
	path = os.path.join(PATH, language)
	if language == 'java':
		java_path = build_language_path('java')
		remove_class_files(path)
		compile_java(java_path) 
	elif language == 'C':
		print "C has no compile script yet"
		print 'inne i c'
	elif language == "C++":
		print "C++ has no compile script yet"
	elif language == 'C#':
		print "C# has no compile script yet"
	elif language == "Python":
		python_path = build_language_path('Python')
		compile_python(python_path)
	else: 	
		print language ++ " is not one of the selected languages, try: java, C, C++, C# or Python"

#remove_class_files()
#compile_language('java')
folder_name = build_language_path('java')
run_java_files(folder_name)


#remove_class_files()
#compile_language("Python")
#compile_python()



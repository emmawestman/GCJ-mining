import os
import subprocess


PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016'))


def run_java_file(filename):
	cmd = ['java ' +filename]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	output, errors = p.communicate()


def build_language_path(language):
	return os.path.join(PATH,language)


def compile_java(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			if (f.endswith(".java")):
				subprocess.check_call(['javac', os.path.join(root,f) ])

def run_java_files(path) :
	problemfolders = [f for f in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, f))]
	for problemfolder in problemfolders:
		problemPATH = os.path.join(PATH, problemfolder)
		userfolders = [f for f in os.listdir(problemPATH) if os.path.isdir(os.path.join(problemPATH, f))]
		for userfolder in userfolders:
			userPATH = os.path.join(problemPATH,userfolder)
			os.chdir(userPATH)
			java_file = [f for f in os.listdir(userPATH) if f.endswith('.java')][0] #TODO: ASSUMES THAT ONLY EXIST ONE JAVA FILE
			class_file =[ f for f in os.listdir(userPATH) if (f.endswith(".class") and f.split('.')[0])==java_file.split('.')[0] ] #TODO : FULT MEN WHAT TO DO
			if len(class_file)>0:
				class_name = class_file[0].split('.')[0]
				run_java_file(class_name)
								

def compile_python(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			subprocess.check_call(['python', os.path.join(root,f) ])



def remove_class_files():
	for root, dirs, files in os.walk(PATH):
		filelist = [ f for f in files if not(f.endswith(".java")) ]
		for f in filelist:			
			os.remove(os.path.join(root,f))

#remove_class_files()		
#compile_java()
#run_java_files(build_language_path('java'))


def compile_language(language):
	path = os.path.join(PATH, language)
	print path 
	if language == 'java':
		remove_class_files(path)
		java_path = build_language_path('java')
		compile_java(java_path) 
	elif language == 'C':
		print "C has no compile script yet"
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
compile_language("Python")
#compile_python()





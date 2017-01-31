import os
import subprocess


PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016','java'))


def run_java_file(filename):
	cmd = ['java ' +filename]
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	output, errors = p.communicate()


def compile_java(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			if (f.endswith(".java")):
				subprocess.check_call(['javac', os.path.join(root,f) ])

def run_java_files() :
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
run_java_files()


def compile_language(language):
	path = os.path.join(PATH, language)
	print path 
	if language == 'java':
		remove_class_files(path)
		compile_java(path) 
	elif language == 'C':
		print "C has no compile script yet"
	elif language == "C++":
		print "C++ has no compile script yet"
	elif language == 'C#':
		print "C# has no compile script yet"
	elif language == "Python":
		compile_python(path)
	else: 	
		print language ++ " is not one of the selected languages, try: java, C, C++, C# or Python"

#remove_class_files()
compile_language("Python")
#compile_python()





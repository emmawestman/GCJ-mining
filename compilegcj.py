import os
import subprocess

PATH = os.path.join('..','solutions_qualification_2016')



def compile_java(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			subprocess.check_call(['javac', os.path.join(root,f) ])

def compile_python(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			subprocess.check_call(['python', os.path.join(root,f) ])



def remove_class_files():
	for root, dirs, files in os.walk(path):
		filelist = [ f for f in files if (f.endswith(".class") or f.endswith(".txt") or f.endswith(".py~")) ]
		for f in filelist:			
			os.remove(os.path.join(root,f))
		

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






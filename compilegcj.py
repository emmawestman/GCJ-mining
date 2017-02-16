import os
import shutil
from compile_java import *
from compile_python import *
from compile_csharp import *
from compile_c import *
from compile_cpp import *
from compile_support_module import *

PATH = os.path.realpath(os.path.join('..','solutions_'))
#PATH_INPUT = os.path.realpath(os.path.join('..','input_'))


					

def compile_language(language, c_id):
	a = -1
	b = -1
	c = -1
	d = -1
	if language == 'java':
		cwd = os.getcwd()
		remove_old_files(language, c_id)
		a, b = compile_java(c_id)
		c, d = run_java_files(c_id)
		os.chdir(cwd)
	elif language == 'C':
		remove_old_files(language, c_id)
		a, b = compile_c(c_id)
		c, d = run_c(c_id)
	elif language == "C++":
		remove_old_files(language, c_id)
		a, b = compile_cpp(c_id)
		c, d = run_cpp(c_id)
	elif language == 'C#':
		remove_old_files(language,c_id)
		#a, b = compile_run_csharp(c_id)
	elif language == "Python":
		a,b = compile_python(c_id)
	else: 	
		print language + " is not one of the selected languages, try: java, C, C++, C# or Python"
	print language + ': ' + str(a) + ' out of ' + str(b) + ' programs compiled sucessfully'
	print language + ': ' + str(c) + ' out of ' + str(d) + ' programs ran sucessfully'
	return a, b, c, d


#input_language = raw_input("what language?")
#c_id = raw_input("which contest id?")

compile_language('Python','6254486')

#compile_language(input_language, c_id)





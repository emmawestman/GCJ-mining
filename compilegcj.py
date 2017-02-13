import os
import shutil
from compile_java import *
from compile_python import *
from compile_csharp import *
from compile_c import *
from compile_cpp import *
from compile_support_module import *

PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016'))
PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))


					

def compile_language(language):
	a = -1
	b = -1
	c = -1
	d = -1
	path = os.path.join(PATH, language)
	if language == 'java':
		remove_old_files(language, path)
		a, b = compile_java(path)
		c, d = run_java_files(path)
	elif language == 'C':
		remove_old_files(language, PATH)
		a, b = compile_c(path)
		c, d = run_c(path)
	elif language == "C++":
		remove_old_files(language, PATH)
		a, b = compile_cpp(path)
		c, d = run_cpp(path)
	elif language == 'C#':
		remove_old_files('cs', path)
		a, b = compile_run_csharp(path)
	elif language == "Python":
		a,b = compile_python(path)
	else: 	
		print language ++ " is not one of the selected languages, try: java, C, C++, C# or Python"
	print language + ': ' + str(a) + ' out of ' + str(b) + ' programs compiled sucessfully'
	print language + ': ' + str(c) + ' out of ' + str(d) + ' programs compiled sucessfully'


input_language = raw_input("what language?")
compile_language(input_language)





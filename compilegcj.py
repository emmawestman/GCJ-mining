import os
import shutil
from compile_java import *
from compile_python import *
from compile_csharp import *
from compile_c import *
from compile_support_module import *

PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016'))
PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))


					

def compile_language(language):
	path = os.path.join(PATH, language)
	if language == 'java':
		remove_old_files(language, path)
		a, b = compile_java(path)
		c, d = run_java_files(path)
		print 'Run: ' + str(c) + '/' + str(d) 
	elif language == 'C' or language == 'C++':
		a, b = compile_c(path)
	#elif language == "C++":
		#compile_c(path)
		# c and c++ can be compiled with the same compiler for now
	elif language == 'C#':
		a, b = compile_run_csharp(path)
	elif language == "Python":
		a,b = compile_python(path)
	else: 	
		print language ++ " is not one of the selected languages, try: java, C, C++, C# or Python"
	print language + ': ' + str(a) + ' out of ' + str(b) + ' programs compiled sucessfully'



input_language = raw_input("what language?")
compile_language(input_language)





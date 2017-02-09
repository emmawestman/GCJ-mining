import os
import shutil
from stuff_module import create_folder
from compile_java import *
from compile_python import *
from compile_csharp import *
from compile_c import *


PATH = os.path.realpath(os.path.join('..','solutions_qualification_2016'))
PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))


					

def compile_language(language):
	path = os.path.join(PATH, language)
	if language == 'java':
		remove_class_files(language, path)
		compile_java(java_path)
		run_java_files(java_path)
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



#compile_language("Python")
#compile_language("C")
compile_language("C++")
#compile_language("C#")



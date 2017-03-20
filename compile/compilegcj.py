import os
import shutil
import sys
import time
from compile_support_module import *
from handle_compilation_errors import *

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from finding_regexes import *
from stuff_module import *


c_path = os.path.join(os.getcwd(), 'compile_c')
sys.path.insert(0, c_path)
from compile_c import *

cpp_path = os.path.join(os.getcwd(), 'compile_c++')
sys.path.insert(0, cpp_path)
from compile_cpp import *

csharp_path = os.path.join(os.getcwd(), 'compile_c#')
sys.path.insert(0, csharp_path)
from compile_csharp import *

'''
java_path = os.path.join(os.getcwd(), 'compile_java')
sys.path.insert(0, java_path)
from compile_java import *
'''


python_path = os.path.join(os.getcwd(), 'compile_python')
sys.path.insert(0, python_path)
from compile_python import *

python_path = os.path.join(os.getcwd(), 'statistics/')
sys.path.insert(0, python_path)
from write_to_csv import *

					

def compile_language(language, p_id, dict):
	if language == 'java':
		#cwd = os.getcwd()
		#dict = compile_java(p_id, dict)
		#dict = run_java_files(p_id,dict)
		print 'not doing java'
	elif language == 'C':
		dict = compile_c(p_id, dict)
		dict = run_c(p_id, dict)
	elif language == "C++":
		dict = compile_cpp(p_id, dict)
		dict = run_cpp(p_id, dict)
	elif language == 'C#':
		dict = compile_run_csharp(p_id, dict)
	elif language == "Python":
		dict = compile_python(p_id, dict)
	else: 	
		print language + " is not one of the selected languages, try: java, C, C++, C# or Python"
	return dict


def compile_all():
	list_of_problem_ids = get_PROBLEM_IDS(gcj_path)
	for PROBLEM_ID in list_of_problem_ids:
		filename = PROBLEM_ID + '.csv'
		dict = read_csv_file(filename)
		for l in ['Python'] :
			print 'Compiles and Runs: ' + l + ' in contest: ' + PROBLEM_ID
			remove_old_files(l, PROBLEM_ID)
			dict = compile_language(l, PROBLEM_ID, dict)
		write_to_csv_file(filename, dict)

compile_all()









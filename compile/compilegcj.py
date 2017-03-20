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
from write_to_csv import *


''''
>>>>>>> Stashed changes
c_path = os.path.join(os.getcwd(), 'compile_c')
sys.path.insert(0, c_path)
from compile_c import *

cpp_path = os.path.join(os.getcwd(), 'compile_c++')
sys.path.insert(0, cpp_path)
from compile_cpp import *

csharp_path = os.path.join(os.getcwd(), 'compile_c#')
sys.path.insert(0, csharp_path)
from compile_csharp import *


>>>>>>> Stashed changes
java_path = os.path.join(os.getcwd(), 'compile_java')
sys.path.insert(0, java_path)
from compile_java import *


python_path = os.path.join(os.getcwd(), 'compile_python')
sys.path.insert(0, python_path)
from compile_python import *


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
    list_of_problem_ids = get_PROBLEM_IDS(os.path.join(os.getcwd(),'../'))
    number_of_problems = len(list_of_problem_ids)
    for i in range(0,number_of_problems):
        PROBLEM_ID = list_of_problem_ids[i]
        filename = PROBLEM_ID + '.csv'
        dict = read_csv_file(filename)
        print 'Compiles and Runs: java ' + ' in contest: ' + PROBLEM_ID
        remove_old_files('java', PROBLEM_ID)
        dict = compile_language('java', PROBLEM_ID, dict)


'''

java_path = os.path.join(os.getcwd(), 'compile_java')
sys.path.insert(0, java_path)
from compile_java import *


def compile_language(language, p_id, dict):
	cwd = os.getcwd()
	#dict = compile_java(p_id, dict)
	run_java_files(p_id,dict)


def compile_all():
    list_of_problem_ids = get_PROBLEM_IDS(os.path.join(os.getcwd(),'../'))
    number_of_problems = len(list_of_problem_ids)
    for i in range(0,number_of_problems):
        PROBLEM_ID = list_of_problem_ids[i]
        filename = PROBLEM_ID + '.csv'
        dict = read_csv_file(filename)
        print 'Compiles and Runs: java ' + ' in contest: ' + PROBLEM_ID
        #remove_old_files('java', PROBLEM_ID)
        compile_language('java', PROBLEM_ID, dict)

compile_all()

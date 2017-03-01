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


cpp_path = os.path.join(os.getcwd(), 'compile_c/')
sys.path.insert(0, cpp_path)
from compile_c import *

cpp_path = os.path.join(os.getcwd(), 'compile_c++/')
sys.path.insert(0, cpp_path)
from compile_cpp import *

csharp_path = os.path.join(os.getcwd(), 'compile_c#/')
sys.path.insert(0, csharp_path)
from compile_csharp import *


java_path = os.path.join(os.getcwd(), 'compile_java/')
sys.path.insert(0, java_path)
from compile_java import *


python_path = os.path.join(os.getcwd(), 'compile_python/')
sys.path.insert(0, python_path)
from compile_python import *

					

def compile_language(language, c_id):
	a = -1
	b = -1
	c = -1
	d = -1
	if language == 'java':
		cwd = os.getcwd()
		a, b = compile_java(c_id)
		c, d = run_java_files(c_id)
		os.chdir(cwd)
	elif language == 'C':
		a, b = compile_c(c_id)
		c, d = run_c(c_id)
	elif language == "C++":
		a, b = compile_cpp(c_id)
		c, d = run_cpp(c_id)
	elif language == 'C#':
		a, b = compile_run_csharp(c_id)
	elif language == "Python":
		a,b = compile_python(c_id)
	else: 	
		print language + " is not one of the selected languages, try: java, C, C++, C# or Python"
	print language + ': ' + str(a) + ' out of ' + str(b) + ' programs compiled sucessfully'
	print language + ': ' + str(c) + ' out of ' + str(d) + ' programs ran sucessfully'
	return a, b, c, d

# compile all languages
print 'Sarting to compile and run all files...'
start = time.time()

list_of_contest_ids = get_CONTEST_IDS()
number_of_contests = len(list_of_contest_ids)

for i in range(0,number_of_contests):
	CONTEST_ID = list_of_contest_ids[i]
	for l in get_LANGUAGE():
		l_start = time.time()
		print 'Compiles and Runs: ' + l + ' in contest: ' + CONTEST_ID
		remove_old_files(l, CONTEST_ID)
		a, b, c, d = compile_language(l, CONTEST_ID)
		l_end = time.time()
		l_diff = l_end - l_start
	

end = time.time()
diff = end - start








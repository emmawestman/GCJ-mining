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


c_path = os.path.join(os.getcwd(), 'compile_c')
sys.path.insert(0, c_path)
from compile_c import *

cpp_path = os.path.join(os.getcwd(), 'compile_c++')
sys.path.insert(0, cpp_path)
from compile_cpp import *

csharp_path = os.path.join(os.getcwd(), 'compile_c#')
sys.path.insert(0, csharp_path)
from compile_csharp import *


java_path = os.path.join(os.getcwd(), 'compile_java')
sys.path.insert(0, java_path)
from compile_java import *


python_path = os.path.join(os.getcwd(), 'compile_python')
sys.path.insert(0, python_path)
from compile_python import *


def compile_language(language, p_id, dict):
    if language == 'java':
        #cwd = os.getcwd()
        compile_java(p_id, dict)
        run_java_files(p_id,dict)
    elif language == 'C':
        compile_c(p_id, dict)
        run_c(p_id, dict)
    elif language == "C++":
        compile_cpp(p_id, dict)
        run_cpp(p_id, dict)
    elif language == 'C#':
        compile_csharp(p_id, dict)
        run_csharp(p_id,dict)
    elif language == "Python":
        #compile_python_files(p_id, dict)
        run_python_files(p_id,dict)
    else:
        print language + " is not one of the selected languages, try: java, C, C++, C# or Python"


def compile_all():
    #python compilegcj.py problem_id size language
    problem = sys.argv[1]
    size = sys.argv[2]
    l = sys.argv[3]
    p_id = problem + '_' + size
    filename = p_id + '.csv'
    dict = read_csv_file(filename)
    print 'Compiles and Runs: ' + l + ' in contest: ' + p_id
    remove_old_files(l, p_id)
    compile_language(l, p_id, dict)
    clean_home_dir()
    write_to_csv_file(filename, dict)

compile_all()

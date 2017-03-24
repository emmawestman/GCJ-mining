import os
import subprocess
import sys
from handle_cpp_errors import *

# import own modules from diffretn directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *
from update_dict import *

gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *
from stuff_module import *

def compile_cpp(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'solutions_' + p_id, 'C++' ))
    
    user_ids = os.listdir(path)
    for user in user_ids :
        user_dict = dict[user]
        user_path = os.path.join(path, user)
        for f in os.listdir(user_path) :
            if has_valid_file_ending('C++', f) :
                print 'compiling c++ file for: ' + user + ' in problem ' + p_id
                exit_code, errors = compile_cpp_command(f, user_path)
                # update dictonary
                print 'FINAL EXIT CODE: ' + str(exit_code)
                set_compile_exitcode(user_dict,exit_code)
                set_compiler_version(user_dict,'-')
                set_run_mesurments('-1', '', user_dict)

def compile_cpp_command(f, user_path) :
    clean_home_dir()
    # do compilation
    exe_file = f.split('.')[0]
    cmd = 'g++ -std=c++0x ' + os.path.join(user_path,f) + ' -o ' + os.path.join(user_path,exe_file)
    exit_code, errors = run_process(cmd)     

    if not (int(exit_code) == 0 or int(exit_code) == 124):
        print 'failed to compile problem'
        print errors
        return handle_compile_errors(errors, exit_code, f, user_path)
    
    else :
        return exit_code, errors

def run_cpp(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'solutions_' + p_id, 'C++' ))
    input_path = os.path.join(get_INPUT_PATH(), p_id + '.in')
    user_ids = os.listdir(path)
    for user in user_ids :
        user_dict = dict[user]
        user_path = os.path.join(path, user)
        filelist = [f for f in os.listdir(user_path) if '.' not in f]
        for f in filelist :
            print 'running c++ file for: ' + user + ' in problem ' + p_id
            exit_code, errors = run_cpp_command(f, user_path, input_path)
            # update dictonary with run mesurments
            set_run_mesurments(exit_code, errors, user_dict)
            # clean dir
            clean_home_dir()
            clean_user_dir(user_path, 'C++')
            

def run_cpp_command(f, user_path, input_path) :
    
    # do run command
    cmd = os.path.join(user_path,f) + ' < ' + input_path
    exit_code, errors = full_exe_cmd(cmd)

    if not (int(exit_code) == 0 or int(exit_code) == 124):
        print 'failed to run problem'
        print errors
        return handle_run_errors(errors, exit_code, f, user_path, input_path)
    
    else :
        return exit_code, errors

def handle_compile_errors(errors, exit_code, f, user_path) :
    if 'error: \'main\' must return \'int\'' in errors :
        print 'REPLACING VOID TO INT IN MAIN'
        replace_void_in_main(user_path, f)
        return compile_cpp_command(f, user_path)
    elif 'error: C++ requires a type specifier for all declarations' in errors :
        print 'ADDING INT TO MAIN'
        add_int_to_main(user_path, f)
        return compile_cpp_command(f, user_path)
    else :
        #we do not /cannnot fix the error
        print 'CANNOT HANDLE!'
        return exit_code, errors

def handle_run_errors(errors, exit_code, f, user_path, input_path) :
    if int(exit_code) == 139 :
        print 'REPLACING INPUT PATH'
        replace_input_path(user_path, f, input_path)
    return exit_code, errors

  







import os
import subprocess
import sys


# import own modules from iffrent directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *
from update_dict import *

gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *


def compile_c_command(exe_path, file_path, user_dict):
    cmd = 'gcc -o ' + exe_path  + ' ' + file_path
    exit_code, errors = run_process(cmd)
    error_code_to_csv = ""
    if 'undefined reference ' in errors :
        error_code_to_csv = " lm "
        exit_code,errors = run_process (cmd + ' -lm')

    if 'only allowed in ' in errors :
        cmd = 'gcc -std=c11 -o' + exe_path  + ' ' + file_path
        if len (error_code_to_csv)>0:
            error_code_to_csv = error_code_to_csv + "&"
        error_code_to_csv = error_code_to_csv + " lm "
        exit_code, errors = run_process(cmd)

    set_compiler_version(user_dict, error_code_to_csv)
    return exit_code,errors

# running the c file
def execute_c_command(exe_path, f, user_path, input_path, user_dict):
    cmd = exe_path + ' < ' + input_path
    exit_code, errors = full_exe_cmd(cmd)
    if 'iostream fatal error' in errors :
        compile_with_gplus_cmd = 'g++ -std=c++0x ' + os.path.join(user_path,f) + ' -o ' + exe_path
        exit_code,errors = full_exe_cmd (os.path.join(user_path,f) + ' < ' + input_path)
    if 'Segmentation fault' in errors :
        exit_code,errors = full_exe_cmd (os.path.join(user_path,f) + ' ' + input_path)

    measure_exe(exe_path,user_dict)
    return exit_code, errors

def measure_exe(exe_path,user_dict):
    try:
        b = str(get_size_of_exe(exe_path))
    except Exception, e:
        b = '-'
    else:
        pass
    finally:
        set_exe_size(user_dict, b)


def compile_c(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'solutions_' + p_id, 'C' ))
    user_ids = os.listdir(path)
    for user in user_ids :
        user_dict = dict[user]
        user_path = os.path.join(path, user)
        for f in os.listdir(user_path) :
            if has_valid_file_ending('C', f) :
                print 'compiling c file for: ' + user + ' in problem ' + p_id

                # do compilation
                exe_file = f.split('.')[0]
                exe_path = os.path.join(user_path,exe_file)
                set_compiler_version(user_dict,'-')

                exit_code,errors = compile_c_command(exe_path,os.path.join(user_path,f),user_dict)
                set_compile_error_msg(user_dict, errors)
                set_compile_exitcode(user_dict,exit_code)
                set_run_mesurments('-1', '', user_dict)




def run_c(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'solutions_' + p_id, 'C' ))
    input_path = os.path.join(get_INPUT_PATH(), p_id + '.in')
    user_ids = os.listdir(path)
    for user in user_ids :
        user_dict = dict[user]
        user_path = os.path.join(path, user)
        filelist = [f for f in os.listdir(user_path) if '.' not in f]
        for f in filelist :
            print 'running c file for: ' + user + ' in problem ' + p_id
            exe_file = f.split('.')[0]
            exe_path = os.path.join(user_path,exe_file)
            # do run command
            exit_code,errors = execute_c_command(exe_path, f, user_path, input_path, user_dict)

            # update dictonary with run mesurments
            #set_run_error_msg(user_dict, errors)
            set_run_mesurments(exit_code, errors, user_dict)

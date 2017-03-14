import os
import subprocess
from handle_python_errors import *
import sys

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *

PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(),'input_'))


def compile_python(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + p_id, 'Python' ))
    print path
    input_path = PATH_INPUT + p_id

    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.py'):
                print 'Runing python file: ' + root
                filename = get_input_file(root)+'.in'
                path_file = os.path.join(root,f)
                path_input = os.path.join(input_path,filename)
                exit_code, errors, dict = run_python_2x(path_file,path_input,p_id,root, dict)
                # update dict compiled 
                dict = set_compile_exitcode(dict,full_path,exit_code)
                dict = do_run_mesurments(exit_code, errors, dict, root)
                
    return dict


def run_python(file_path,path_input,pythonversion,dict):
    print "Running file python3 " + file_path
    args = ' < ' + path_input
    return run_python_command(pythonversion,file_path, args, dict)


def run_python_2x(file_path,path_input,p_id,root, dict):
    exit_code, errors, dict = run_python(file_path,path_input,'python')
    if not int(exit_code) == 0 or not int(exit_code) == 124:
        return handle_python_2x_errors(file_path,path_input,p_id,root,errors,dict)             
    return exit_code, errors, dict


def run_python_3x(file_path,path_input,p_id,root,dict):
    exit_code, errors, dict = run_python(file_path,path_input,'python3')
    if len(errors) > 0:
        return handle_python_3x_errors(errors,file_path,path_input,p_id,root,dict)
    return exit_code, errors, dict

def run_python_command(pythonversion,path_file,args,dict):    
    if pythonversion == 'python3 ' :
        version = "3.5"
    else:
        version = "2.7"
    # update dictonry so verison is stored in csv
    dict = set_compiler_version(dict,full_path,version)

    cmd = pythonversion + path_file + args
    exit_code, errors = full_exe_cmd(cmd)
    return exit_code, errors, dict

def handle_python_2x_errors(file_path,path_input,p_id,root,errors,dict):
    error_name = get_error_name(errors)
    if error_name =='ImportError':
        flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip')
        if flag == 0:
            return run_python_3x(file_path,path_input,p_id,root,dict)
        return run_python_2x(file_path,path_input,p_id,root)    
    elif error_name == 'SyntaxError':
        return run_python_3x(file_path,path_input,p_id,root,error, dict)
    elif error_name =='FileNotFoundError' or error_name == 'IOError':
        handle_python_file_not_found(path_input,root,p_id,file_path)
        return run_python_2x(file_path,path_input,p_id,root,dict)
    elif error_name == 'IndexError':
        args = ' ' + path_input +' '+os.path.join(root,'output.txt')
        exit_code, errors, dict = run_python_command('python ',file_path,args,dict)
        if len(errors) == 0:
            return exit_code, errors, dict
    print errors

def handle_python_3x_errors(errors,file_path,path_input,p_id,root,dict):
    error_name = get_error_name(errors)
    if error_name =='ImportError':
        flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip3')
        print 'handle python 3: ' + missing_module_name
        if flag == 1:
            return run_python_3x(file_path,path_input,p_id,root,dict)
    elif error_name =='FileNotFoundError' or error_name =='IOError':
        handle_python_file_not_found(path_input,root,p_id,file_path)
        run_python_3x(file_path,path_input,p_id,root,dict)
    print errors



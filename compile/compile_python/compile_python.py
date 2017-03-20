import os
import subprocess
from handle_python_errors import *
import sys

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *

compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from update_dict import *



def compile_python(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'solutions_' + p_id, 'Python' ))
    print path
    input_path = os.path.join(get_INPUT_PATH(), p_id + '.in')
    user_ids = os.listdir(path)
    for user in user_ids :
        user_dict = dict[user]
        user_path = os.path.join(path, user)
        #files = os.listdir(user_path)
        files = [f for f in os.listdir(user_path) if f.endswith('.py')]
        for f in files :
            print 'Runing python file: ' + f + ' for user: ' + user + ' in p_id: ' + p_id
            if ' ' in f :
                f = f.replace(' ', '\ ')
            path_file = os.path.join(user_path, f)
            print 'FILE PATH: ' + path_file
            exit_code, errors = run_python_2x(path_file, input_path,p_id, user_path, user_dict)
            # update dict compiled 
            set_run_mesurments(exit_code, errors, user_dict)
    return dict

def run_python(file_path,path_input,pythonversion,user_dict):
    print "Running file python " + file_path
    args = ' < ' + path_input
    return run_python_command(pythonversion,file_path, args, user_dict)


def run_python_2x(file_path,path_input,p_id,root, user_dict):
    exit_code, errors = run_python(file_path,path_input,'python ', user_dict)
    if not int(exit_code) == 0 or not int(exit_code) == 124 :
        return handle_python_2x_errors(file_path,path_input,p_id,root,errors,user_dict)             
    return exit_code, errors


def run_python_3x(file_path,path_input,p_id,root,user_dict):
    exit_code, errors = run_python(file_path,path_input,'python3 ', user_dict)
    print 'EXIT CODE ' + str(exit_code)
    if not int(exit_code) == 0 or not int(exit_code) == 124:
        return handle_python_3x_errors(errors,file_path,path_input,p_id,root,user_dict)
    return exit_code, errors

def run_python_command(pythonversion,path_file,args,user_dict):
    if pythonversion == 'python3 ' :
        version = "3.5"
    else:
        version = "2.7"
    # update dictonry so verison is stored in csv
    set_compiler_version(user_dict, version)
    cmd = pythonversion + path_file + args
    exit_code, errors = full_exe_cmd(cmd)
    return exit_code, errors

def handle_python_2x_errors(file_path,path_input,p_id,root,errors,user_dict):
    error_name = get_error_name(errors)
    if error_name =='ImportError':
        flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip')
        print flag
        print missing_module_name
        if flag == 0:
            return run_python_3x(file_path,path_input,p_id,root,user_dict)
        return run_python_2x(file_path,path_input,p_id,root, user_dict)    
    elif error_name == 'SyntaxError':
        return run_python_3x(file_path,path_input,p_id,root, user_dict)
    elif error_name =='FileNotFoundError' or error_name == 'IOError':
        handle_python_file_not_found(path_input,root,p_id,file_path)
        return run_python_2x(file_path,path_input,p_id,root,user_dict)
    elif error_name == 'IndexError':
        args = ' ' + path_input +' '+os.path.join(root,'output.txt')
        exit_code, errors = run_python_command('python ',file_path,args,user_dict)
        #if not int(exit_code) == 0 or not int(exit_code) == 124:
        return exit_code, errors
    elif error_name == 'OSError' :
        return exit_code, errors
    else :
        # we can don't  fix problem and do not try agian
        print errors
        return exit_code, errors 
        

def handle_python_3x_errors(errors,file_path,path_input,p_id,root,user_dict):
    error_name = get_error_name(errors)
    if error_name =='ImportError':
        flag,missing_module_name = handle_import_error(file_path,path_input,errors,'pip3')
        print 'handle python 3: ' + missing_module_name
        print flag
        if flag == str(1):
            return run_python_3x(file_path,path_input,p_id,root,user_dict)
        else :
            print 'give up'
            print errors
            return exit_code, errors
    elif error_name =='FileNotFoundError' or error_name =='IOError':
        handle_python_file_not_found(path_input,root,p_id,file_path)
        run_python_3x(file_path,path_input,p_id,root,user_dict)
    else :
        # we can don't  fix problem and do not try agian
        print 'CAN NOT HANDLE ERROR'
        print errors
        return exit_code, errors 
        



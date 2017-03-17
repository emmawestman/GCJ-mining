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
                cmd = 'timeout 30s g++ ' + os.path.join(root,f) + ' -o ' + os.path.join(user_path,f.split('.')[0]))
                exit_code, errors = run_process(cmd)    

                # update dictonary
                set_compile_exitcode(user_dict,root,exit_code)
                set_compiler_version(user_dict,root,'-')
        
                if not int(exit_code) == 0:
    				print 'failed to run problem: ' + root
    				print errors

	return dict


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

			# do run command
            cmd = 'timeout 30s ' + os.path.join(user_path,f) + ' < ' + input_path
            exit_code, errors = full_exe_cmd(cmd)

            # update dictonary with run mesurments
            do_run_mesurments(exit_code, errors, user_dict)
	return dict




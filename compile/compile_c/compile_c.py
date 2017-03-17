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
    for root, dirs, files in os.walk(path):
        for f in files :
            if has_valid_file_ending('C', f) :
                user, filename = get_compile_info('C', root, f)
                print 'compiling c file for: ' + user + ' in problem ' + p_id
                
                # do compilation
                cmd = 'timeout 30s g++ ' + os.path.join(root,f) + ' -o ' + os.path.join(root,filename)
                exit_code, errors = run_process(cmd)    

                # update dictonary
                dict = set_compile_exitcode(dict,root,exit_code)
                dict = set_compiler_version(dict,root,'-')
        
                if not int(exit_code) == 0:
    				print 'failed to run problem: ' + root
    				print errors

	return dict


def run_c(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'solutions_' + p_id, 'C' ))
    PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'input_' + p_id))
    for root, dirs, files in os.walk(path):	
        # only try to run the executable 
        filelist = [f for f in files if '.' not in f]
        for f in filelist:
            user, input_file = get_run_info('C', root)
            print 'running c file for: ' + user + ' in problem ' + p_id

			# do run command
            cmd = 'timeout 30s ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT, input_file)
            exit_code, errors = full_exe_cmd(cmd)

            # update dictonary with run mesurments
            dict = do_run_mesurments(exit_code, errors, dict, root)
	return dict




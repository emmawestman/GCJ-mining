import os
import subprocess
import sys


# import own modules from iffrent directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *

gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *



	
def compile_c(c_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C' ))
    #number of files that successfylly compiles
    succes_nbr = 0
    nbr_of_files = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            nbr_of_files += 1
            print 'compiling c file nbr: ' + str(nbr_of_files)
            user, filename = get_compile_info('C', root, f)
            cmd = 'timeout 30s g++ ' + os.path.join(root,f) + ' -o ' + os.path.join(root,filename)
	
            exit_code, errors = run_process(cmd)
            # update user dict
            user_id = get_user_id(os.path.join(root,f))
            suser_dict = dict[user_id]
            user_dict['compiler_version'] = '-'
            if int(exit_code) == 0:
				if 'warning' not in errors:
					print 'failed to run problem: ' + root
					print errors
					user_dict['compiled'] = 'NO'
				else:
					succes_nbr += 1
					user_dict['compiled'] = 'YES'
	return succes_nbr, nbr_of_files, dict


def run_c(c_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C' ))
    PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(),'input_' + c_id))
    succes_nbr = 0
    nbr_of_files = 0
    for root, dirs, files in os.walk(path):	
        # only try to run the executable 
        filelist = [f for f in files if '.' not in f]
        for f in filelist:
            nbr_of_files += 1
            print 'running c file nbr: ' + str(nbr_of_files)
			
            user, input_file = get_run_info('C', root)
		
            cmd = 'timeout 30s ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT, input_file)
            exit_code, errors = full_exe_cmd(cmd)
            if int(exit_code) == 0 :
                succes_nbr += 1
            # update dictonary with run mesurments
            do_run_mesurments(exit_code, errors, dict, root)
	return succes_nbr, nbr_of_files, dict



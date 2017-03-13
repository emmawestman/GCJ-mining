import os
import subprocess
import sys

# import own modules from diffretn directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *

gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *

def compile_cpp(c_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C++' ))
    #number of files that successfylly compiles
    succes_nbr = 0
    nbr_of_files = 0
    print path

    file1 = open('cpp_errors.txt', "a")
    file1.write(path + '\n')
    for root, dirs, files in os.walk(path):
        for f in files:
            nbr_of_files += 1
            print 'compiling c++ file nbr: ' + str(nbr_of_files)
            
            user, filename = get_compile_info('C++', root, f)
            cmd = ['timeout 30s g++ -std=c++0x ' + os.path.join(root,f) + ' -o ' + os.path.join(root,filename)]
            exit_code, errors = exe_cmd(cmd)
            # update user dict
            user_id = get_user_id(os.path.join(root,f))
            user_dict = dict[user_id]
            user_dict['compiler_version'] = '-'
            # no timeout
            if int(exit_code) == 0:
                print 'success!'
                succes_nbr += 1
                user_dict['compiled'] = 'YES'
            else :
                print 'Error: ' + exit_code + ' for file: ' + os.path.join(root,f)
                user_dict['compiled'] = 'NO'
                
                
    return succes_nbr, nbr_of_files, dict



def run_cpp(c_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C++' ))
    PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(),'input_' + c_id))
    succes_nbr = 0
    nbr_of_files = 0
    for root, dirs, files in os.walk(path):    
        # only try to run the executable 
        filelist = [f for f in files if '.' not in f]
        for f in filelist:
            nbr_of_files += 1
            print 'running c ++ file nbr: ' + str(nbr_of_files)
            
            user, input_file = get_run_info('C++', root)
        
            cmd = ['timeout 30s ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,input_file)]
            exit_code, errors = exe_cmd(cmd)
            # no timeout
            if int(exit_code) == 0:
                print 'success!'
                succes_nbr += 1
            else :
                print 'Error: ' + exit_code + ' for file: ' + os.path.join(root,f)
            # wirite mesuremnts to csv
            user_dict = dict[user]
            mesurements = get_mesurments(errors)    
            write_to_user_dict(user_dict, exit_code, mesurments)

    return succes_nbr, nbr_of_files, dict



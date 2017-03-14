
import os
import subprocess
import re
import sys
from handle_compile_errors_csharp import *
from handle_run_errors_csharp import *

# import own modules from iffrent directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *
gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from stuff_module import *
from constants import *
from finding_regexes import *



def compile_run_csharp(c_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C#' ))
    PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(),'input_' + c_id))
    succes_nbr = 0
    nbr_of_files = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.cs'):
                nbr_of_files += 1
                print 'Compiling problem: ' + root
                # update user dict
                user_id = get_user_id(os.path.join(root,f))
                print user_id
                user_dict = dict[user_id]
                user_dict['compiler_version'] = '-'

                filename = get_input_file(root)+'.in'
                input_file = os.path.join(PATH_INPUT,filename)
                succes_of_file = compile_and_run_csharp(root,f,None,input_file,None,dict) # REALLY COMPILE AND RUN CSHARP
                succes_nbr += succes_of_file
                
                if succes_of_file == 1 :
                    user_dict['compiled'] = 'YES'
                else :
                    user_dict['compiled'] = 'NO'

    return succes_nbr, nbr_of_files, dict


def build_arguments (flag,csharp_file_p,csharp_file_p_dependecy,root,dict):
    csharp_file = ''
    if flag is not None:
        csharp_file = '-r:'+flag+'.dll '
        # update th dict with the used flag
        user_id = get_user_id(csharp_file_p)
        user_dict['compiler_version'] = flag
    csharp_file+= os.path.join(root,csharp_file_p)
    if csharp_file_p_dependecy is not None :
        csharp_file = csharp_file + ' ' + os.path.join(root,csharp_file_p_dependecy)
    
    return csharp_file

def compile_and_run_csharp(root,csharp_file_p,csharp_file_p_dependecy,input_file,flag,dict):
    csharp_file = build_arguments (flag, csharp_file_p, csharp_file_p_dependecy,root,dict)
    cmd = 'mcs ' + csharp_file
    exit_code, errors = run_process(cmd)
    if not exit_code == 0:
        return handle_compilation_errors(errors, root,csharp_file_p,csharp_file_p_dependecy,input_file, flag, dict)
    csharp_exe= csharp_file_p.replace('.cs','.exe')
    if csharp_file_p_dependecy is not None:
        csharp_file_p = csharp_file_p_dependecy
    return run_csharp(input_file,root,os.path.join(root,csharp_exe),csharp_file_p, dict)


def run_csharp_command(csharp_exe,input_file):
    if input_file is not None :
        csharp_exe = csharp_exe + ' < ' + input_file
    cmd = 'mono ' + csharp_exe 
    return full_exe_cmd(cmd)
 


def run_csharp(input_file,root,csharp_exe,original_class_file, dict):
    exit_code, errors = run_csharp_command(csharp_exe,input_file)
    if not exit_code == 0:
        handle_run_errors(errors, root, original_class_file, input_file, dict)
    # update dictonary
    user = get_user_id(root)
    user_dict = dict[user]
    mesurements = get_mesurments(errors)    
    write_to_user_dict(user_dict, exit_code, mesurments)
    return 1


def handle_compilation_errors(errors, root,csharp_file_p,csharp_file_p_dependecy,input_file, flag, dict):
    if "does not contain a static `Main' method suitable for an entry point" in errors:  
        create_main_file(root, csharp_file_p, input_file)
        return compile_and_run_csharp (root,'TestMain.cs',csharp_file_p,input_file,flag, dict)
    if 'The type or namespace name' in errors:
        old_regex = filter_information('\`\w+\'',None,errors)[0]
        old_regex = old_regex.replace('`','')
        old_regex = old_regex.replace ('\'','')
        new_regex = filter_information('\`\w+[.]\w+\'',None,errors)
        if len(new_regex)>0 :
            new_regex = new_regex[0]
            new_regex = new_regex.replace('`','')
            new_regex = new_regex.replace ('\'','')
            return compile_and_run_csharp (root,csharp_file_p,csharp_file_p_dependecy,input_file,new_regex, dict)
    print errors
    return 0

def handle_run_errors(errors, root, original_class_file, input_file, dict):
    error_name = filter_information('Unhandled Exception:\n\w+\.\w+\.\w+',':',errors)
    if error_name and error_name[0].replace('\n','') == ('System.IO.DirectoryNotFoundException' or 'System.IO.FileNotFoundException') and input_file is not None:
        remove_files_in_a_user_solution(root)
        change_input_streams(input_file,os.path.join(root,original_class_file),root)
        return compile_and_run_csharp(root,original_class_file,None,None,None, dict)
    print errors
    # update dictonary with run mesurments
    do_run_mesurments(exit_code, errors, dict, root)
    return 0





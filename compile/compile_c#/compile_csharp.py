
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
from update_dict import *

gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from stuff_module import *
from constants import *
from finding_regexes import *



def compile_run_csharp(c_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C#' ))
    PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(),'input_' + c_id))

    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.cs'):
 
                filename = get_input_file(root)+'.in'
                input_file = os.path.join(PATH_INPUT,filename)
                exit_code, errors, dict = compile_and_run_csharp(root,f,None,input_file,None,dict) # REALLY COMPILE AND RUN CSHARP
                
                # update dictonary, copiler version is set in build argumets to set correct flag 
                dict = set_compile_exitcode(dict,full_path,exit_code)
                dict = do_run_mesurments(exit_code, errors, dict, root)
                
    return dict


def build_arguments (flag,csharp_file_p,csharp_file_p_dependecy,root,dict):
    csharp_file = ''
    dict = set_compiler_version(dict,full_path,'-')
    if flag is not None:
        csharp_file = '-r:'+flag+'.dll '
        # update the dict with the used flag
        dict = set_compiler_version(dict,full_path,flag)
    csharp_file+= os.path.join(root,csharp_file_p)
    if csharp_file_p_dependecy is not None :
        csharp_file = csharp_file + ' ' + os.path.join(root,csharp_file_p_dependecy)
    
    return csharp_file, dict

def compile_and_run_csharp(root,csharp_file_p,csharp_file_p_dependecy,input_file,flag,dict):
    csharp_file, dict = build_arguments (flag, csharp_file_p, csharp_file_p_dependecy,root,dict)
    cmd = 'mcs ' + csharp_file
    exit_code, errors = run_process(cmd)
    if not exit_code == 0:
        handle_compilation_errors(errors, root,csharp_file_p,csharp_file_p_dependecy,input_file, flag, dict)
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
    return exit_code, errors, dict


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

def handle_run_errors(errors, root, original_class_file, input_file, dict):
    error_name = filter_information('Unhandled Exception:\n\w+\.\w+\.\w+',':',errors)
    if error_name and error_name[0].replace('\n','') == ('System.IO.DirectoryNotFoundException' or 'System.IO.FileNotFoundException') and input_file is not None:
        remove_files_in_a_user_solution(root)
        change_input_streams(input_file,os.path.join(root,original_class_file),root)
        return compile_and_run_csharp(root,original_class_file,None,None,None, dict)
    print errors
 





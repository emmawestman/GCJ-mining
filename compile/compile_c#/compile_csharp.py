
import os
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
from constants import *


def compile_csharp(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection', 'solutions_' + p_id, 'C#' ))
    user_ids = os.listdir(path)
    for user in user_ids :
        user_dict = dict[user]
        user_path = os.path.join(path, user)
        files = os.listdir(user_path)
        files = [f for f in os.listdir(user_path) if f.endswith('.cs')]
        input_path = os.path.join(get_INPUT_PATH(), p_id + '.in')
        if len(files) == 2 :
            f = files[0]
            f_dep = files[1]
            exit_code, errors = compile_one_file_csharp(user_path,f,f_dep,input_path,None,user_dict) # REALLY COMPILE AND RUN CSHARP
        elif len(files) == 1:
            f = files[0]
            f_dep = None
            exit_code, errors = compile_one_file_csharp(user_path,f,f_dep,input_path,None,user_dict) # REALLY COMPILE AND RUN CSHARP
        else:
            set_compiler_version(user_dict, '-')
            exit_code = -1
            errors = ''

        # update dictonary, copiler version is set in build argumets to set correct flag
        set_exe_size(user_dict, '-')
        set_compile_exitcode(user_dict,exit_code)
        set_run_mesurments('-1', '', user_dict)

    return dict

def compile_csharp_command(csharp_full_cmd):
    cmd = 'mcs ' + csharp_full_cmd
    print "CMD " + cmd
    return run_process(cmd)

def get_user_compilation_flag(user_dict):
    flag = user_dict['compiler_version']
    if flag == '-':
        return None
    return flag

def build_arguments (flag,csharp_file_p,csharp_file_p_dependecy,root,user_dict):
    csharp_args = ''
    if flag is None :
        #set flag to '-'
        set_compiler_version(user_dict, '-')
    else:
        # update the dict with the used flag
        set_compiler_version(user_dict,flag)
    return build_path_args (flag,root,csharp_file_p,csharp_file_p_dependecy)


def build_path_args (flag,root,csharp_file_p,csharp_file_p_dependecy):
    csharp_args = ''
    if flag is not None:
        csharp_args = '-r:'+flag+'.dll '
    csharp_args+= os.path.join(root,csharp_file_p)
    if csharp_file_p_dependecy is not None :
        csharp_args = csharp_args + ' ' + os.path.join(root,csharp_file_p_dependecy)
    return csharp_args


def compile_one_file_csharp(root,csharp_file_p,csharp_file_p_dependecy,input_file,flag,user_dict):
    csharp_file = build_arguments (flag, csharp_file_p, csharp_file_p_dependecy,root,user_dict)
    exit_code,errors = compile_csharp_command(csharp_file)
    if int(exit_code) == 0 or int(exit_code) == 124 :
        return exit_code,errors
    return handle_compilation_errors(exit_code,errors,root,csharp_file_p,csharp_file_p_dependecy,input_file,flag, user_dict)


def handle_compilation_errors(error_code,errors,root,csharp_file_p,csharp_file_p_dependecy,input_file, flag, user_dict):
    print 'IN HANDLE COMPILE ERRORS'
    print errors
    if 'The type or namespace name' in errors and 'System.Numerics' in errors:
        return compile_csharp_command(build_arguments('System.Numerics',csharp_file_p,csharp_file_p_dependecy,root,user_dict))
    if 'The type or namespace name' in errors and 'System.Drawing' in errors:
        return compile_csharp_command(build_arguments('System.Drawing',csharp_file_p,csharp_file_p_dependecy,root,user_dict))
    if 'The type or namespace name' in errors and 'System.Windows' in errors :
        return compile_csharp_command(build_arguments('System.Windows',csharp_file_p,csharp_file_p_dependecy,root,user_dict))
    if 'does not contain a static' in errors : # absence of main fucntion
        print "MISSING MAIN " + root + ' ' + csharp_file_p
        all_functions = filter_candidate_functions(root,csharp_file_p)
        if len(all_functions)>0:
            for func in all_functions:
                create_main_file(root,csharp_file_p,input_file, func)
                #Create main creates TestMain, hence original class file becomes dependency_files#
                compile_csharp_command(build_path_args(flag,root,'TestMain.cs',csharp_file_p,))
                exit_code,errors = run_csharp_command(os.path.join(root,'TestMain.exe'),input_file, user_dict)
                if exit_code == 0 or exit_code == 124 or exit_code == -1 :
                    return error_code,errors #success
    return error_code,errors


def run_csharp(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection', 'solutions_' + p_id, 'C#' ))
    input_file = os.path.join(get_INPUT_PATH(), p_id + '.in')
    user_ids = os.listdir(path)
    for user in user_ids :
        user_dict = dict[user]
        user_path = os.path.join(path, user)
        print user_path
        csharp_exe = [f for f in os.listdir(user_path) if f.endswith('.exe')] #ONLY ONE C# executable
        if len (csharp_exe)>0:
            csharp_exe = csharp_exe[0]
            csharp_org =[ f for f in os.listdir(user_path) if f.endswith(".cs") and f.split('.')[0] ==csharp_exe.split('.')[0]][0]
            dependency_files =[ f for f in os.listdir(user_path) if f.endswith(".cs") and (f.split('.')[0] != csharp_exe.split('.')[0])]
            dependency_file = dependency_files[0] if len (dependency_files) >0 else None
            exit_code,errors=run_csharp_solution(input_file,user_path,csharp_exe,dependency_file,csharp_org,get_user_compilation_flag(user_dict),user_dict)
            print exit_code
            print errors
        # update dictonary, copiler version is set in build argumets to set correct flag
        else :
            exit_code = '-1'
            errors = ''
        set_run_mesurments(exit_code, errors, user_dict)



def run_csharp_command(csharp_exe,input_file,user_dict):
    cmd = 'mono ' + csharp_exe + ' < ' + input_file
    print cmd
    error_code,errors = full_exe_cmd(cmd)
    print csharp_exe
    try:
        b = str(get_size_of_exe(csharp_exe))
        print b
    except Exception, e:
        b = '-'
    finally:
        set_exe_size(user_dict, b)
    print errors
    return error_code,errors


def run_csharp_solution(input_file,root,csharp_exe,dependency_file,csharp_org,flag,user_dict):
    exit_code, errors = run_csharp_command(os.path.join(root,csharp_exe),input_file,user_dict)
    if not exit_code == 0 or not exit_code == 124 or not exit_code == -1 :
        return handle_run_errors(exit_code,errors, root, dependency_file, input_file,csharp_org,csharp_exe,flag,user_dict)
    return exit_code, errors



def handle_run_errors(error_code, errors, root,csharp_file_p_dependecy,input_file,original_class_file,csharp_exe,flag,user_dict):
    if 'System.IO.DirectoryNotFoundException' in errors or 'System.IO.FileNotFoundException' in errors:
        print original_class_file
        print csharp_file_p_dependecy
        change_input_streams(input_file,os.path.join(root,original_class_file),root)
        if csharp_file_p_dependecy is not None :
            change_input_streams(input_file,os.path.join(root,csharp_file_p_dependecy),root)
        compile_csharp_command(build_path_args(flag,root,original_class_file,csharp_file_p_dependecy))
        return run_csharp_command(os.path.join(root,csharp_exe),input_file,user_dict)
    return error_code,errors

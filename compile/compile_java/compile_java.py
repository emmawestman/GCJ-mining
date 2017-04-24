import os
import subprocess
import sys
from handle_java_run_errors import *

# import own modules from diffrent directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *
from update_dict import *
gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *


def set_compile_mesurments(user_dict, b, exit_code):
    set_exe_size(user_dict, b)
    set_compile_exitcode(user_dict,exit_code)

def run_java_file(root,class_name,p_id, user_dict):
    path_to_input = os.path.abspath(os.path.join(get_INPUT_PATH(), p_id + '.in'))
    error_code, errors = run_java_command(build_run_args(root,class_name,path_to_input,' < '))

    if (int (error_code) == 0) or (int (error_code) == 124):
        return error_code, errors
    return handle_java_run_errors(errors,error_code,root,class_name,path_to_input, user_dict)



def build_run_args(root,class_name,path_to_input,pipe):
    args = pipe + path_to_input
    return root + ' ' +class_name + ' ' + args


def run_java_command(args):
    cmd = 'java -classpath ' + args
    return full_exe_cmd(cmd)

def compile_java_command(full_path):
    cmd = 'javac ' + full_path
    exit_code, errors = run_process(cmd)
    exe_path = full_path.split('.')[0]
    try:
        b = str(get_size_of_exe(exe_path))
    except Exception, e:
        b = '-'
    return b, exit_code, errors

def compile_java(p_id, dict):
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection','solutions_' + p_id, 'java' ))
    print path
    for root, dirs, files in os.walk(path):
        for f in files:
            if (f.endswith(".java")):
                print "compiling java " + f
                full_path = os.path.join(root,f)
                b, exit_code, errors = compile_java_command(full_path)
                # write compile statistics
                if 'is public, should be declared in a file named' in errors :
                    rename_class_file(full_path,errors)
                    b,exit_code,errors = compile_java_command(full_path)
                user_dict = dict[get_user_id(root)]
                user_dict = dict[get_user_id(root)]
                #default mesurments
                set_compiler_version(user_dict,'-')
                set_run_mesurments('-1', '', user_dict)
                print 'COPILE EXIT CODE ' + str(exit_code)
                print errors
                set_compile_mesurments(user_dict, b, exit_code)


def handle_java_run_errors(errors,exit_code,root,class_name,input_path, user_dict):
    #print errors
    file_path = os.path.join(root,class_name+'.java')
    if 'Main method not found' in errors :
        #call fix main to file
        return exit_code, errors
    elif 'Could not find or load main class' in errors :
        remove_missing_package(file_path)
        b, exit_code, errors = compile_java_command(os.path.join(root,class_name+'.java'))
        set_compile_mesurments(user_dict, b, exit_code)
        return run_java_command(build_run_args(root,class_name,input_path,' < '))
    elif 'FileNotFoundException' in errors :
        rename_fileread_filewrite(file_path,input_path,root)
        b, exit_code, errors = compile_java_command(file_path)
        set_compile_mesurments(user_dict, b, exit_code)
        return run_java_command(build_run_args(root,class_name,input_path,' < '))
    elif 'ExceptionInInitializerError' in errors :
        return run_java_command(build_run_args(root,class_name,input_path,''))
    return exit_code, errors




def run_java_files(p_id,dict) :
    path = os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection','solutions_' + p_id, 'java'))
    userfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    for user_folder in userfolders:
        userPATH = os.path.join(path,user_folder)
        user_dict = dict[user_folder]
        #Filter class name
        java_file = [f for f in os.listdir(userPATH) if f.endswith('.java')][0] #TODO: ASSUMES THAT ONLY EXIST ONE JAVA FILE
        class_file =[ f for f in os.listdir(userPATH) if (f.endswith(".class") and f.split('.')[0])==java_file.split('.')[0] ] #TODO : FULT MEN WHAT TO DO
        if len(class_file)>0:
            class_name = class_file[0].split('.')[0]
            print "running " + userPATH + " " + class_name
            error_code,errors = run_java_file(userPATH,class_name,p_id, user_dict)
            print 'FINAL ERROR CODE: ' + str(error_code)
            print errors
            set_run_mesurments(error_code,errors,user_dict)

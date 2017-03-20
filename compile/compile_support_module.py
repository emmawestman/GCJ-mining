import os
import shutil

import subprocess
import re
import sys

# import own modules from iffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from stuff_module import create_folder



def get_input_file(root):
    return re.search('\d+\_\d', root).group(0)

def get_contents_of_file(file_path):
    file_manager = open(file_path,'r')
    file_contents = file_manager.read()
    file_manager.close()
    return file_contents

def write_new_contents_to_the_file(file_path,file_contents):
    #write changes
    file_manager=open(file_path,'w')
    file_manager.write(file_contents)
    file_manager.close()


#language is the file ending for the language
def remove_old_files(language, c_id):
    language_path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, language))
    for root, dirs, files in os.walk(language_path):
        if language == 'C++' or language == 'C':
            # remove executable files for c++ an c
            filelist = [f for f in files if '.' not in f]
        elif language == 'Python':
            filelist = [ f for f in files if (f == '.py' ) ]

        # remove extra created main files
        elif language == 'C#':
            filelist = [ f for f in files if (f == 'TestMain.cs' or f.endswith('.exe')) ]
        else:
            filelist = [ f for f in files if not(f.endswith(language)) ]
        # remove the files!
        for file in filelist:
            os.remove(os.path.join(root,file))


def remove_all_old_files() :
    for c_id in get_CONTEST_IDS() :
        for l in get_LANGUAGE() :
            remove_old_files(l, c_id)

def get_user_id(path) :
    index = re.findall("/\w+", path)
    user_idx = len(index)-2
    user = index[user_idx]
    user_id = user[1:]
    return user_id


def get_compile_info(regexp, root, f):
    index = root.find(regexp)
    filename = root[index+len(regexp):]
    index = filename.find('/')
    user = filename[index+1:]
    index = f.find('.')
    name = f[:index]
    return user, name

def get_run_info(regexp, root):
    index = root.find(regexp)
    filename = root[index+len(regexp)+1:]
    index = filename.find('/')
    user = filename[index+1:]
    filename = filename[:index]    
    input_file = filename + '.in'     
    return user, input_file

# to run with flags
def full_exe_cmd(cmd) :
    #full_cmd = "/usr/bin/time -f \"%x,%e,%U,%S,%K,%M,%t,%F,%O,%I,%W\" sh -c \"" + cmd + "\""
    full_cmd = cmd
    return run_process(full_cmd)

# to compile
def run_process(cmd):
    #cmd_timeout = 'timeout 30s ' + cmd
    #full_cmd = [cmd_timeout]
    full_cmd = [cmd]
    p = subprocess.Popen(full_cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()
    exit_code = p.returncode
    return exit_code, errors








def has_valid_file_ending(language, f):
    if f.endswith(".java") and language == 'java':
        return True 
    elif f.endswith(".c") and language == 'C':
        return True
    elif (f.endswith(".cpp") or f.endswith(".C") or f.endswith(".cc") or f.endswith(".CPP") or f.endswith(".c++") or f.endswith(".cp") or f.endswith(".cxx")) and language == 'C++':
        return True
    elif f.endswith(".cs") and language == 'C#':
        return True
    elif f.endswith(".py") and language == 'Python':
        return True
    else:
        print 'found file without maching ending: ' + f 
        return False







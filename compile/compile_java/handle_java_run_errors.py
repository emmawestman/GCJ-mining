import os
import sys
import re

compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from handle_compilation_errors import *

def rename_class_file(file_path,errors):
    real_name_regex = '(\w+\.java)\n'
    real_name = re.findall(real_name_regex,errors)[0]
    new_file_path = file_path.split('/')[:-1]
    new_file_path = '/'+ reduce(os.path.join,new_file_path)+'/'+real_name
    os.rename(file_path,new_file_path)

def remove_missing_package(file_path):
    rename_stuff_in_file ('package\s.*','',file_path,1)

def rename_fileread_filewrite (file_path,input_path,root) :
    inregex = [ 'new Scanner\(new File\((\"?[\w+-]*\.?\w+\"?)\)', 'new FileInputStream\(new File\((\"?[\w+-]*\.?\w+\"?)\)\)', 'FileInputStream\((\"?\w+\.?\w+\"?)\)', 'new FileReader\(new File\((\"?[\w+-]*\.?\w+\"?)\)\)', 'new BufferedReader\(new FileReader\((\"?[\w+-]*\.?\w+\"?)\)','(?:new FileReader\()([\"]?(?:[\w]\:)?(?:[\w+-]+)[\"]*\n?(?:.*)(?:[\"]))(?:[\)])']
    new_input = '\"' +  input_path + '\"'
    outregex = ['new FileWriter\(.*\)','new PrintWriter\(.*\)']
    new_output= 'new PrintWriter(new File(\"' + os.path.join(root,'output.txt') + '\"))'
    handle_file_not_found_java(inregex,new_input,outregex,new_output,file_path)

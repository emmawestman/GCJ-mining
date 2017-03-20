import os
import sys

compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from handle_compilation_errors import *


def remove_missing_package(file_path):
    rename_stuff_in_file ('package\s.*','',file_path,1)

def rename_fileread_filewrite (file_path,input_path,root) :
    inregex = [ 'new Scanner\(new File\w+\((\"?\w+\.?\w+\"?)\)\);', '(?:new FileReader\()([\"]?(?:[\w]\:)?(?:[\w+-]+)[\"]*\n?(?:.*)(?:[\"]))(?:[\)])', 'new FileReader\(.*?\)']
    new_input = '\"' +  input_path + '\"'
    outregex = ['new FileWriter\(.*\)','new PrintWriter\(.*\)']
    new_output= 'new PrintWriter(new File(\"' + os.path.join(root,'output.txt') + '\"))'
    handle_file_not_found_java(inregex,new_input,outregex,new_output,file_path)

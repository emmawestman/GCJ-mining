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
    inregex = [ '(new Scanner\(new File\()\"?[\w+-]*\.?\w+\"?(\))','(new Scanner\(new File\()\"?[\w+\s]+\"?.?[\w]*\"?(\)\s?\))', '(new FileInputStream\(new File\()\"?[\w+-]*\.?\w+\"?(\)\))', '(FileInputStream\()\"?[\w:\\\\]*\w+\.?\w+\"?(\))', '(new FileReader\(new File\()\"?[\w+-]*\.?\w+\"?(\)\))','(new FileReader\(new File\()[\n\s]*\"?[/\w+]+.?\w+\"?(\)\))', '(new FileReader\s?\()\"?[\w+-]*\.?\w+\"?(\))','(new FileReader\(new File\()[\w+.\(\)\s]+\"?.?\w*?\"(\)\))','(new FileReader\()[\"]?(?:[\w]\:)?(?:[\w+-]+)[\"]*\n?(?:.*)(?:[\"])(\))','(new FileReader\(new File\().*(\)\))']
    new_input = '\"' +  input_path + '\"'
    handle_file_not_found(file_path,inregex,new_input)
    out_regex = ['(new FileWriter\()\"?[\w+]\"?[\w]*.?[\w]*\"?(\))','(new FileOutputStream(\s?new File\()\"?\s?[\w+\s]*\"?[\w]*.?[\w]*/"?(\s?\)\s?))','(new BufferedReader\()\"?[\w+]\"?[\w]*.?[\w]*\"?(\))']
    open('output.txt', 'w').close()
    new_out_put = '\"' + 'output.txt' + '\"'
    handle_file_not_found(file_path,out_regex,new_out_put)

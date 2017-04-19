import os
import re
import sys

# import own modules from iffrent directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *

def remove_files_in_a_user_solution(root):
	files = os.listdir(root)
	filelist = [ f for f in files if (f == 'TestMain.cs' or f.endswith('.exe')) ]
	for file in filelist:
		os.remove(os.path.join(root,file))

def create_main_file(root,csharp_file_p,input_file,static_func):
	full_path = os.path.join(root,csharp_file_p)
	namespace = find_namespace(full_path)
	# create main file and call some function...
	csharp_main(static_func, csharp_file_p, namespace, root,input_file)


def find_namespace(full_path):
	file_contentes = get_contents_of_file(full_path)
	return re.search('(?:namespace)\s((?:\w+.)+?(?:\w+))', file_contentes).group(0)

def csharp_main(full_function_decl, csharp_filename, namespace,root,input_file):
	filename =  csharp_filename.split('.')[0]
	function_name = re.findall(r'(\w+)',full_function_decl)[0]
	main_file = os.path.join(root, 'TestMain.cs')
	print main_file
	file_content = namespace + '\n' + '{\n    class TestMain \n    {\n        static void Main() \n        {\n            ' + filename + '.' + function_name + build_main_function(full_function_decl,input_file) + '\n        }\n    }\n}'
	write_new_contents_to_the_file(main_file,file_content)

#ONLY CHOOSING STATIC FUNCTIONS
def filter_candidate_functions(root,csharp_file_p):
	file_path = os.path.join(root,csharp_file_p)
	file_contents = get_contents_of_file(file_path)
	p = re.compile('static\s(?:int|void|long|string)\s(\w+\([\w+\s]*?\))')
	return p.findall(file_contents)

#ONLY HANDLING ONE StreamWriter and StreamReader
def build_main_function(filtered_function,input_file):
	main_string = '('
	p = re.compile('(\w+\s\w+)')
	list_of_args = p.findall(filtered_function)
	for x in range(0,len(list_of_args)) :
		group = list_of_args[x]
		arg_type = group.split(' ')[0]
		arg_decl = ''
		if arg_type == 'StreamReader':
			arg_decl = 'new StreamReader(\''+ input_file + '\')'
		if arg_type == 'StreamWriter':
			arg_decl = 'new StreamWriter(output.txt)'
		main_string+= arg_decl
		if x != len(list_of_args)-1 and ',' in main_string:
			main_string+= ','
	main_string+=');'
	return main_string

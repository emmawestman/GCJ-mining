# Error handling for c++
import os
import sys

# import own modules from diffretn directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *
from handle_compilation_errors import *

regexes_cpp = ['(freopen ?\()\"?[\w+-]*\.?\w+\"?(,[ ]*?\"r\",[ ]*?stdin\))', '(fopen ?\()\"?[\w+-]*\.?\w+\"(,[ ]*?\"r\"\))']


def replace_void_in_main(user_path, f) :
	file_path = os.path.join(user_path, f)
	content = get_contents_of_file(file_path)
	content = content.split('\n')
 	for idx, line in enumerate(content) :
		if 'void main' in line :
			line = line.replace('void', 'int')
			content[idx] = line
			break
	content = '\n'.join(content)
	#print content
	write_new_contents_to_the_file(file_path, content)

def add_int_to_main(user_path, f) :
	file_path = os.path.join(user_path, f)
	content = get_contents_of_file(file_path)
	content = content.split('\n')
 	for idx, line in enumerate(content) :
		if 'main' in line :
			line = 'int ' + line
			content[idx] = line
			break
	content = '\n'.join(content)
	write_new_contents_to_the_file(file_path, content)

def replace_input_path(user_path, f, input_path) :
	file_path = os.path.join(user_path, f)
	new_input = "\"" + input_path + "\""
	handle_file_not_found(file_path,regexes_cpp,new_input)

from handle_compilation_errors import *
import re

def create_main_file(root,csharp_file_p,input_file):
	full_path = os.path.join(root,csharp_file_p)
	namespace = find_namespace(full_path)
	# create main file and call some function...
	filter_candidates = filter_candidate_functions(full_path)
	csharp_main(filter_candidates[0], csharp_file_p, namespace, root,input_file)


def change_input_streams(input_file,csharp_file,root):
	file_contents = get_contents_of_file(file_path
	list_of_inregexes = ['new StreamReader\((.*)\)']
	new_file_input = '\"'+input_file+'\"'
	list_of_outregexes = ['new StreamWriter\((.*)\)']
	new_file_output = '\"' + os.path.join(root,'output.txt') + '\"'
	handle_file_not_found(file_path,list_of_regexes,new_input,new_output)
	
def rename_input_file(input_file,csharp_file,errors):
	old_regex = filter_information('\".*?\"',None,errors)[0]
	old_regex = old_regex.split('.')[-1]
	new_regex = input_file
	rename_stuff_in_file(new_regex,old_regex,csharp_file)

def find_namespace(full_path):
	file_contentes = get_contents_of_file(file_path)
	return re.search('r(?:namespace)\s\w+').group(0)

def csharp_main(full_function_decl, csharp_filename, namespace,root,input_file):
	filename =  csharp_filename.split('.')[0]
	function_name = re.findall(r'(\w+)',full_function_decl)[0]
	main_file = os.path.join(root, 'TestMain.cs')         
	file_content = 'namespace ' + namespace + '\n' + '{ \n class TestMain \n { \n static void Main() \n { \n' + filename + '.' + function_name + build_main_function(full_function_decl,input_file) + ' \n } \n } \n }'
	write_new_contents_to_the_file(main_file,file_content)

#ONLY CHOOSING STATIC FUNCTIONS
def filter_candidate_functions(file_path):
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

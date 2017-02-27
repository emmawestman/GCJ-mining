
def create_main_file():
	namespace = find_namespace(csharp_file_p, root)
	# create main file and call some function...
	filter_candidates = filter_candidate_functions(os.path.join(root,csharp_file_p))
	print 'FUNCTION ' + filter_candidates[0]
	csharp_main(filter_candidates[0], csharp_file_p, namespace, root,input_file)



def change_input_streams(input_file,csharp_file,root):
	file_manager = open(csharp_file, "r")
	contents = file_manager.read()
	file_manager.close()
	old_input = re.findall(r'new StreamReader\((.*)\)',contents)[0]
	new_file_input = '\"'+input_file+'\"'
	new_file_contents = contents.replace(old_input,new_file_input)
	file_manager=open(csharp_file,'w')
	file_manager.write(new_file_contents)
	file_manager.close()
	file_manager = open(csharp_file, "r")
	contents = file_manager.read()
	file_manager.close()
	old_input = re.findall(r'new StreamWriter\((.*)\)',contents)[0]
	new_file_input = '\"' + os.path.join(root,'output.txt') + '\"'
	new_file_contents = contents.replace(old_input,new_file_input)
	file_manager=open(csharp_file,'w')
	file_manager.write(new_file_contents)
	file_manager.close()
	


def rename_input_file(input_file,csharp_file,errors):
	old_regex = filter_information('\".*?\"',None,errors)[0]
	old_regex = old_regex.split('.')[-1]
	new_regex = input_file
	rename_stuff_in_file(new_regex,old_regex,csharp_file)



def csharp_main(full_function_decl, filename, namespace, path,input_file):
	index = len(filename) -3
	filename = filename[:index]
	function_name = re.findall(r'(\w+)',full_function_decl)[0]
	main_file= os.path.join(path, 'TestMain.cs')         
	file1 = open(main_file, "w")
	file_content = 'namespace ' + namespace + '\n' + '{ \n class TestMain \n { \n static void Main() \n { \n' + filename + '.' + function_name + build_main_function(full_function_decl,input_file) + ' \n } \n } \n }'
	file1.write(file_content)
	file1.close()

#ONLY CHOOSING STATIC FUNCTIONS
def filter_candidate_functions(file_path):
	file_manager = open(file_path,'r')
	file_contents = file_manager.read()
	list_of_stuff = []
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

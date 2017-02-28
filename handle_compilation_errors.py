import re
from compile_support_module import *

def find_old_regex(regex_list,file_contents):
	for regex in regex_list:
		old_regex = find_out_what_regex(regex,file_contents)
		print old_regex
		if len(old_regex)>0:
			return old_regex
	return []

def find_out_what_regex(regex,file_contents):
	return re.findall(regex,file_contents)

def rename_input_file(regex_list,new_input,file_contents):
	old_input = find_old_regex(regex_list,file_contents)
	for oi in old_input :
		what_to_replace = re.search(r'\((.*?)\)',oi).group(1)
		print "WHAT TO REPLACE " + what_to_replace
		file_contents = file_contents.replace(what_to_replace,new_input)
	return file_contents

def rename_output_file(regex_list,new_output,file_contents):
	old_input = find_old_regex(regex_list,file_contents)
	for oi in old_input :
		what_to_replace = re.search(r'\((.*?)\)',oi).group(1)
		file_contents = file_contents.replace(what_to_replace,new_output)
	return file_contents


def handle_file_not_found(file_path,list_of_possible_inregexes,list_of_outregexes,new_input,new_output):
	file_contents = get_contents_of_file(file_path)
	changed_contents = rename_input_file(list_of_possible_inregexes,new_input,file_contents)
	changed_contents = rename_output_file(list_of_outregexes,new_output,changed_contents)
	write_new_contents_to_the_file(file_path,changed_contents)




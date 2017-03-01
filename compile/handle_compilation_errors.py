import re
from compile_support_module import *

def find_old_regex(regex_list,file_contents):
	for key in regex_list:
		old_regex = find_out_what_regex(key,file_contents)
		if len(old_regex)>0:
			return old_regex
	return 

def find_out_what_regex(regex,file_contents):
	found_matches = []
	for match in re.finditer(regex,file_contents):
		found_matches.append(match.group(0))
	return found_matches

def rename_input_file(regex_list,new_input,contents):
	old_input = find_old_regex(regex_list,contents)
	for oi in old_input :
		new_file_contents = contents.replace(oi,new_input)
	return new_file_contents

def rename_output_file(regex,new_output,file_contents):
	old_input = re.findall(regex,file_contents)
	if len(old_input)>0:
		old_input = old_input[0]
		file_contents = contents.replace(old_input,new_input,file_input)
	return file_contents


def handle_file_not_found(file_path,list_of_possible_inregexes,list_of_outregexes,new_input,new_output):
	file_contents = get_contents_of_file(file_path)
	changed_contents = rename_input_file(list_of_possible_inregexes,new_input,file_contents)
	changed_contents = rename_output_file(list_of_outregexes,new_output,changed_contents)
	write_new_contents_to_the_file(file_path,changed_contents)




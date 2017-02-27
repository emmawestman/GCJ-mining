import re

def find_old_new_regex(regex_list,file_contents):
	for key in regex_list:
		old_regex = find_out_what_regex(key,file_contents)
		if len(old_regex)>0:
			return old_regex,value
	return 

def find_out_what_regex(regex,file_contents):
	found_matches = []
	for match in re.finditer(regex,file_contents,r.S)
		found_matches.append(match.group(0))
	return found_matches

def rename_input_file(regex_list,contents):
	old_input,new_input = find_old_new_regex(regex_list,file_contents)
	new_file_contents = contents.replace(old_input,new_input)
	return new_file_contents

def rename_output_file(regex,new_output,file_contents,root):
	old_input = re.findall(regex,file_contents)
	if len(old_input)>0:
		old_input = old_input[0]
		file_contents = contents.replace(old_input,new_input,file_input)
	return file_contents

import re

def find_old_new_regex(regex_dict,file_contents):
	for key, value in regex_dict.iteritems():
		old_regex = find_out_what_regex(key,file_contents)
		if old_regex is not None:
			return old_regex,value


def find_out_what_regex(regex,file_contents):
	found_matches = re.search(regex,file_contents)
	if found_matches is not None:
		match = found_matches.group(0)
		return match
	return None

def rename_input_file(regex_dict,contents):
	old_input,new_input = find_old_new_regex(regex_dict,file_contents)
	new_file_contents = contents.replace(old_input,new_input)
	return new_file_contents

def rename_output_file(regex,new_output,file_contents,root):
	old_input = re.findall(regex,file_contents)
	if len(old_input)>0:
		old_input = old_input[0]
		file_contents = contents.replace(old_input,new_input,file_input)
	return file_contents

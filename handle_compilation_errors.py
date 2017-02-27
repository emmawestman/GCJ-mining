import re

def find_old_new_regex(regex_list,file_contents):
	for item in regex_list:
		found_matches = find_out_what_regex(item,file_contents)
		if found_matches is not None:
			return found_matches
	return None

def find_out_what_regex(regex,file_contents):
	found_matches = re.search(regex,file_contents)
	if found_matches is not None:
		match = found_matches.group(0)
		return match
	return None	

def rename_inorout_file(regex_list,input_file,file_contents):
	found_match = find_old_new_regex(regex_list,file_contents)
	if found_match is not None:
			copyofmatch = found_match
			find_what_to_replace = re.search(r'\((.*?)\)',found_match).group(1)
			new_input = found_match.replace(find_what_to_replace,input_file)
			file_contents = file_contents.replace(copyofmatch,new_input)
	return file_contents


#error = 'Traceback (most recent call last): File "b.py", line 3, in <module> import os, sys, ljqpy, time ImportError: No module named ljqpy'
#res = find_out_what_regex('named\s(\w+)', error)
#print res
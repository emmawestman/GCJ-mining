import re
from compile_support_module import *
import sys

def find_old_regex(regex_list,file_contents):
	for regex in regex_list:
		print "WHAT REGEX " + regex

		old_regex = find_out_what_regex(regex,file_contents)
		if len(old_regex)>0:
			return old_regex
	return []

def find_out_what_regex(regex,file_contents):
	return re.findall(regex,file_contents)

def rename_inputoutput_file(regex_list,new_input,file_contents):
	old_input = find_old_regex(regex_list,file_contents)
	for oi in old_input :
		what_to_replace = re.search(r'\((.*?)\)',oi).group(1)
		file_contents = file_contents.replace(what_to_replace,new_input)
	return file_contents




def rename_file_not_found_java(regex_list,new_input,file_contents):
	old_input = find_old_regex(regex_list,file_contents)
	for oi in old_input :
		print "WHAT WAS FOUND "
		print oi
		print "WHA TO REPLACE " + new_input
		file_contents = file_contents.replace(oi,new_input)
	return file_contents

def handle_file_not_found_java(regex_list_input,new_input,regex_list_output,new_output,file_path):
	file_contents = get_contents_of_file(file_path)
	file_contents = rename_file_not_found_java(regex_list_input,new_input,file_contents)
	#file_contents = rename_file_not_found_java(regex_list_output,new_output,file_contents)
	write_new_contents_to_the_file(file_path,file_contents)

def rename_stuff_in_file (old_string,new_string,file_path,counter):
	file_contents = get_contents_of_file(file_path)
	changed_contents = re.sub(old_string,new_string,file_contents,counter)
	write_new_contents_to_the_file(file_path,changed_contents)

def handle_file_not_found(file_path,list_of_possible_inregexes,list_of_outregexes,new_input,new_output):
	file_contents = get_contents_of_file(file_path)
	changed_contents = rename_inputoutput_file(list_of_possible_inregexes,new_input,file_contents)
	changed_contents = rename_inputoutput_file(list_of_outregexes,new_output,changed_contents)
	write_new_contents_to_the_file(file_path,changed_contents)

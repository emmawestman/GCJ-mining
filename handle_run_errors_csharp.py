

def handle_run_errors():
	error_name = filter_information('Unhandled Exception:\n\w+\.\w+\.\w+',':',errors)
	if error_name and error_name[0].replace('\n','') == ('System.IO.DirectoryNotFoundException' or 'System.IO.FileNotFoundException') and input_file is not None:
		remove_files_in_a_user_solution(root)
		change_input_streams(input_file,os.path.join(root,original_class_file),root)
		return compile_csharp(root,original_class_file,None,None,None)
	print errors
	return 0

from handle_compilation_errors import *




def change_input_streams(input_file,csharp_file,root):
	file_path = os.path.join(root, csharp_file)
	list_of_inregexes = ['new (?:System.IO.)?StreamReader\(((?:\"@).*?)\)','new (?:System.IO.)?StreamReader\((.*)?\)\)','File.ReadLines\((.*?)\)?\)','File.ReadAllLines\((.*)\)','System.IO.File.ReadAllText\((.*?)\)','File.ReadAllText\((.*?)\)','File.OpenText\((.*?)\)']
	new_file_input = '\"'+input_file+'\"'
	list_of_outregexes = ['new StreamWriter\((.*)\)']
	new_file_output = '\"' + os.path.join(root,'output.txt') + '\"'
	handle_file_not_found_java(list_of_inregexes,new_file_input,list_of_outregexes,new_file_output,file_path)

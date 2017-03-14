import re

def get_user_id(path) :
	index = re.findall("/\w+", path)
	user_idx = len(index)-2
	user = index[user_idx]
	user_id = user[1:]
	return user_id

def set_column_in_user_dict(dict,full_path,column,value):
	user_id = get_user_id(full_path)
	user_dict = dict[user_id]
	user_dict[column] = value
	return dict

def set_compile_exitcode(dict,full_path,exit_code) :
	return set_column_in_user_dict(dict,full_path,'compiled',exit_code)

def set_compiler_version(dict,full_path,version) :
	return set_column_in_user_dict(dict,full_path,'compiler_version',version)

def get_mesurments(errors) :
    regex = "\,\d?\.?\d*"
    res = [] 
    output = re.findall(regex, errors)
    #remove first comma
    for s in output :
        res.append(s[1:])
    return res

def write_to_user_dict(user_dict, exit_code, mesurments):
    user_dict['exit_code'] = exit_code
    user_dict['wall_clock'] = mesurments[0]
    user_dict['user_time'] = mesurments[1]
    user_dict['syatem_time'] = mesurments[2]
    user_dict['avg_memory'] = mesurments[3]
    user_dict['max_RAM'] = mesurments[4]
    user_dict['avg_RAM'] = mesurments[5]
    user_dict['nbr_page_faults'] = mesurments[6]
    user_dict['nbr_file_out'] = mesurments[7]
    user_dict['nbr_file_in'] = mesurments[8]
    user_dict['swap_main_memory'] = mesurments[9]

def set_run_mesurments(exit_code, errors, dict, root) :
    user = get_user_id(root)
    user_dict = dict[user]
    mesurements = get_mesurments(errors)    
    write_to_user_dict(user_dict, exit_code, mesurments)

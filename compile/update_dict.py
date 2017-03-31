import re

def get_user_id(path) :
    return path.split('/')[-1]

def set_column_in_user_dict(user_dict,column,value):
    user_dict[column] = str(value)

def set_compile_exitcode(user_dict,exit_code) :
    return set_column_in_user_dict(user_dict,'compiled',exit_code)

def set_compiler_version(user_dict,version) :
    return set_column_in_user_dict(user_dict,'compiler_version',version)

def get_mesurments(errors) :
    regex = "\,\d?\.?\d*"
    res = []
    output = re.findall(regex, errors)
    print errors
    #remove first comma
    for s in output :
        res.append(s[1:])
    return res

def write_to_user_dict(user_dict, exit_code, mesurments):
    user_dict['exit_code'] = exit_code
    if not len(mesurments) == 10 :
        user_dict['wall_clock'] = '-'
        user_dict['user_time'] = '-'
        user_dict['system_time'] = '-'
        user_dict['avg_memory'] = '-'
        user_dict['max_RAM'] = '-'
        user_dict['avg_RAM'] = '-'
        user_dict['nbr_page_faults'] = '-'
        user_dict['nbr_file_out'] = '-'
        user_dict['nbr_file_in'] = '-'
        user_dict['swap_main_memory'] = '-'
    else :
        user_dict['wall_clock'] = mesurments[0]
        user_dict['user_time'] = mesurments[1]
        user_dict['system_time'] = mesurments[2]
        user_dict['avg_memory'] = mesurments[3]
        user_dict['max_RAM'] = mesurments[4]
        user_dict['avg_RAM'] = mesurments[5]
        user_dict['nbr_page_faults'] = mesurments[6]
        user_dict['nbr_file_out'] = mesurments[7]
        user_dict['nbr_file_in'] = mesurments[8]
        user_dict['swap_main_memory'] = mesurments[9]
    return dict

def set_run_mesurments(exit_code, errors, user_dict) :
    mesurments = get_mesurments(errors)
    return write_to_user_dict(user_dict, exit_code, mesurments)

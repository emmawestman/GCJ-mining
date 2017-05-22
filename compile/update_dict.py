import re

def get_user_id(path) :
    return path.split('/')[-1]

def set_column_in_user_dict(user_dict,column,value):
    user_dict[column] = str(value)

def set_exe_size(user_dict, size):
    set_column_in_user_dict(user_dict,'exe_size', size)

def set_compile_exitcode(user_dict,exit_code) :
    set_column_in_user_dict(user_dict,'compiled',exit_code)

def set_compiler_version(user_dict,version) :
    set_column_in_user_dict(user_dict,'compiler_version',version)

def remove_unwanted_chars(msg):
    if '\t' in msg :
         msg = msg.replace('\t', ' ')
    if '^' in msg :
         msg = msg.replace('^', ' ')
    if ',' in msg :
         msg = msg.replace(';', ' ')
    return msg


def format_error_msg(msg) :
    msg = remove_unwanted_chars(msg)
    if  'error' in msg :
         index = msg.find('error')
         index = msg[index:].find(':')
         msg = msg[index:]
         print 'Error found: ' + msg
    if len(msg) > 80 :
        msg = msg[0:80]
    if len(msg) == 0 :
        msg = '-'
    return msg


def format_run_msg(msg, lang) :
    # remove last two lines, cotains mesured data
    lines = msg.split('\n')
    lines = lines[:-2]
    msg = ' '.join(lines)
    if lang == 'Java':
        index1 = msg.find('java')
        index2 = msg[index1:].find(' ')
        msg = msg[index1:index2]
    elif lang == 'Python':
        msg = format_error_msg(msg)
    elif lang == 'C#':
        index1 = msg.find(':')
        index2 = msg[index1:].find(':')
        msg = msg[index1:index2]
    else :
        index = msg.find('error')
        msg = msg[index:]
    if len(msg) > 80 :
        msg = msg[0:80]
    return msg


def set_compile_error_msg(user_dict, msg):
    msg = format_error_msg(msg)
    print 'Writing: ' + msg
    set_column_in_user_dict(user_dict,'compile_error_msg', msg)

def set_run_error_msg(user_dict, msg, exit_code, lang):
    if str(exit_code) == '-15' :
        msg = 'Timeout'
    else :
        if len(msg) == 0 :
             msg = '-'
        else :
            msg = format_run_msg(msg, lang)
    print 'Writing: ' + msg
    set_column_in_user_dict(user_dict,'run_error_msg', msg)

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

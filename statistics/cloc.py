import os
import subprocess
import sys


# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *

LANGUAGE = get_LANGUAGE()


# creates on row with prob_id, langage, user, blank, comment, code
def cloc_file(prob_id, lang, user) :
    user_path  = os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection', 'solutions_' + prob_id, lang, user))
    print user_path
    all_files = os.listdir(user_path)
    if len(all_files)>1:
        cmd = ['cloc ' + user_path ]
    else:
        file_name = all_files[0]
        if " " in file_name :
            without_blanks = file_name.split()
            new_name="".join(without_blanks)
            os.rename(os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection', 'solutions_' + prob_id, lang, user,file_name)),  os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection', 'solutions_' + prob_id, lang, user,new_name)))
            file_name = new_name
        fil = os.path.realpath(os.path.join(get_HOME_PATH(),'datacollection', 'solutions_' + prob_id, lang, user,file_name))
        cmd = ["cat " + fil + " |tr \"\r\" \"\n\"|" + "cloc --stdin-name=" + fil + " -" ]
    print cmd
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()
    print output
    print errors
    data = [int(s) for s in output.split() if s.isdigit()]
    if len(data) != 3 :
        result =  [str(data[-3]), str(data[-2]), str(data[-1])]
    else :
        result = ['-', '-', '-']

    print result
    return result

# creates a file containing rows with the format describen in cloc_problem
def cloc_problem() :
    user = sys.argv[1]
    problem = sys.argv[2]
    size = sys.argv[3]
    p_id = problem + '_' + size
    print 'CLOC for ' + str(p_id)
    dict = read_csv_file(str(p_id) + '.csv')
    results = (cloc_file(p_id, 'C++', user))
    # update user dict
    if results[2] == '1' :
        results[2] = '-'
    user_dict = dict[user]
    user_dict['cloc'] = results[2]
    user_dict['blanks'] = results[0]
    user_dict['comments'] = results[1]
    # write to dict to file
    write_to_csv_file(str(p_id) + '.csv', dict)

def clean_all_zeros() :
    one_up = os.path.join(os.getcwd(), '../')
    for problem_id in get_PROBLEM_IDS(one_up):
        print problem_id
        dict = read_csv_file(str(problem_id) + '.csv')
        users = dict.keys()
        for user in users :
            user_dict = dict[user]
            cloc_val = user_dict['cloc']
            if str(cloc_val) == '0' :
                user_dict['cloc'] = '-'
        write_to_csv_file(str(problem_id) + '.csv', dict)



# calcualte cloc for all contests
def cloc_all() :
    # one dir up
    one_up = os.path.join(os.getcwd(), '../')
    for problem_id in get_PROBLEM_IDS(one_up):
        cloc_problem(problem_id)

cloc_problem()
#clean_all_zeros()

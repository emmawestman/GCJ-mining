'''Script for dowloading all solutions to Qualification Round 2016'''

import urllib2
import os
import sys

# import own modules from iffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from finding_regexes import *
from stuff_module import *


io_set_id_0 = "0";
io_set_id_1 = "1"

dict = {}

def build_user_id_url(contest_id,pos):
   return get_BASE()+contest_id+'/scoreboard'+'/do/?cmd=GetScoreboard&contest_id='+contest_id+'&show_type=all&start_pos='+pos

def build_downloadproblem_url(contest_id,problem,io_set_id,username) :
   return get_BASE()+contest_id+'/scoreboard'+'/do/?cmd=GetSourceCode&problem='+problem+'&io_set_id='+ io_set_id+'&username='+username


def retrive_users(url):
    answer = urllib2.urlopen(url)
    page = answer.read()
    return filter_information('\"n\"\:\s*\"\w+\"',':',page)

def retrieve_sol(contest_id,problem,io_set_id,username):
    requesturl = build_downloadproblem_url(contest_id,problem,io_set_id,username)
    answer = urllib2.urlopen(requesturl).read()
    if answer.startswith('Server Error'):
        return
    else :
        path = os.path.join(get_HOME_PATH(),'datacollection','solutions_'+ problem+'_'+io_set_id)
        create_folder(path)
        with open(os.path.join(path,username),'w') as f:
            f.write(answer)


def download_one_page(problem_id,contest_id,page_number):
    user_id_url = build_user_id_url(contest_id,str(page_number))
    all_users_id = retrive_users(user_id_url)
    list_of_items = ['0','1']
    for item in list_of_items :
        for user in all_users_id:
            print "downloading solution " + contest_id + ' ' + problem_id + ' ' + user +' page nbr '+ page_number
            retrieve_sol(contest_id,problem_id,item,user)		


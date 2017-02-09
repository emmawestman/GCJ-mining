'''Script for dowloading all solutions to Qualification Round 2016'''

import urllib2
import os
from stuff_module import *
from finding_regexes import *
CONTEST_PATH = 'https://code.google.com/codejam/contests.html'

io_set_id_0 = "0";
io_set_id_1 = "1"


def build_user_id_url(base_url,contest_id,pos):
   return base_url+'/do/?cmd=GetScoreboard&contest_id='+contest_id+'&show_type=all&start_pos='+pos

def build_downloadproblem_url(base_url,problem,io_set_id,username) :
   return base_url+'/do/?cmd=GetSourceCode&problem='+problem+'&io_set_id='+ io_set_id+'&username='+username


def retrive_users(url):
    answer = urllib2.urlopen(url)
    page = answer.read()
    return filter_information('\"n\"\:\s*\"\w+\"',':',page)

def retrieve_sol(base_url,problem,io_set_id,username):
    requesturl = build_downloadproblem_url(base_url,problem,io_set_id,username)
    answer = urllib2.urlopen(requesturl).read()
    if answer.startswith('Server Error'):
        return
    else :
        path = os.path.join('..','solutions_qualification_2016')
        create_folder(path)
        os.chdir(path)
        with open(username+'_'+problem+'_'+io_set_id,'w') as f:
            f.write(answer)

def download_one_page_solutions(base_url,list_of_problems,user_id_url):
    all_users_id = retrive_users(user_id_url)
    list_of_items = ['0','1']
    for problem in list_of_problems :
        for user in all_users_id :
			for item in list_of_items :
				retrieve_sol(base_url,problem,item,user)
				print 'problem ' + problem + ' item ' + item + ' user ' + user


def download_all_pages(base_url,list_of_problem_ids,contest_id):
	i = 1
	while (i<10): #TODO: FIX THIS LIMIT AND CHANGE TO FOR-LOOP
		print 'dowloading solutions from ' + str(i)
		user_id_url = build_user_id_url(base_url,contest_id,str(i))
		print user_id_url
		download_one_page_solutions(base_url,list_of_problem_ids,user_id_url)
		i = i+30


def get_all_contests_id():
	answer = urllib2.urlopen(CONTEST_PATH).read()
	list_of_duplicates = filter_information('contest/[\d]+/dashboard','/',answer)
	return list(set(list_of_duplicates))



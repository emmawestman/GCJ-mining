'''Script for dowloading all solutions to Qualification Round 2016'''

import urllib2
import os
from lxml import etree
#import shutil


problem_id_url = "https://code.google.com/codejam/contest/6254486/scoreboard#vf=1" #extract problem id
exampleurl = "https://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetSourceCode&problem=5652388522229760&io_set_id=0&username=Lewin"
user_id_url = "http://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetScoreboard&contest_id=6254486&show_type=all&start_pos=1" #extract user id

io_set_id_0 = "0";
io_set_id_1 = "1"

def build_base_url(contest_id):
   return 'https://code.google.com/codejam/contest/'+contest_id+'/scoreboard'


def build_user_id_url(base_url,contest_id,pos):
   return base_url+'/do/?cmd=GetScoreboard&contest_id='+contest_id+'&show_type=all&start_pos='+pos

def build_downloadproblem_url(base_url,problem,io_set_id,username) :
   return base_url+'/do/?cmd=GetSourceCode&problem='+problem+'&io_set_id='+ io_set_id+'&username='+username

def retrive_problem_ids(url):
    page = urllib2.urlopen(url).read()
    return filter_information("\"id\":",page)

def retrive_users(url):
    answer = urllib2.urlopen(url)
    page = answer.read()
    return filter_information("\"n\":",page)

def filter_information (regex,page):
    remaining_page = page
    ids = []
    while regex in remaining_page:
	index = remaining_page.find(regex)
	index += len(regex)
	remaining_page = remaining_page[index:]
	# finding the start qutation mark for problem id
	start_index = remaining_page.find("\"")
	# find the end qutation marl for problem id
	end_index = remaining_page[start_index+1:].find("\"")
	# extract problem id string
	item = remaining_page[start_index+1:end_index+2]
	ids.append(item)
	
	remining_page = remaining_page[end_index+3:]
	
    return ids


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

def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError:
         if os.path.exists(folder):
             pass
         else: 
             raise

def download_one_page_solutions(base_url,list_of_problems,user_id_url):
    all_users_id = retrive_users(user_id_url)
    list_of_items = ['0','1']
    for problem in list_of_problems :
        for user in all_users_id :
			for item in list_of_items :
				retrieve_sol(base_url,problem,item,user)
				print 'problem ' + problem + ' item ' + item + ' user ' + user


def download_all_pages(contest_id):
	base_url =  build_base_url(contest_id)
	list_of_problem_ids = retrive_problem_ids(base_url)
	i = 1
	while (i<10): #TODO: FIX THIS LIMIT AND CHANGE TO FOR-LOOP
		print 'dowloading solutions from ' + str(i)
		user_id_url = build_user_id_url(base_url,contest_id,str(i))
		print user_id_url
		download_one_page_solutions(base_url,list_of_problem_ids,user_id_url)
		i = i+30

#READ FROM INPUT FILE 
number_of_contests=int(raw_input())
for cas in xrange(0,number_of_contests):
    contest_id=(raw_input())
    download_all_pages(contest_id)


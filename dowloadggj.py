'''Script for dowloading all solutions to Qualification Round 2016'''

import urllib2
import os
from lxml import etree
#import shutil


baseurl = "https://code.google.com/codejam/contest/6254486/scoreboard#vf=1"
exampleurl = "https://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetSourceCode&problem=5652388522229760&io_set_id=0&username=Lewin"
userurl = "http://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetScoreboard&contest_id=6254486&show_type=all&start_pos=1"

io_set_id_0 = "0";
io_set_id_1 = "1"

PROBLEM_A = '5652388522229760'
PROBLEM_B = '5634697451274240'
PROBLEM_C = '5738606668808192'
PROBLEM_D = '5636311922769920'


def retrive_problem_ids(page):
    return filter_information("\"id\":",page)

def retrive_users(page):
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
	#print remaining_page[start_index-10:end_index+10]
	print item
	
    return ids


def retrieve_sol(problem,io_set_id,username):
    requesturl = 'https://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetSourceCode&problem='+problem+'&io_set_id='+ io_set_id+'&username='+username
    return urllib2.urlopen(reuqesturl)

def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError as exs :
         if exc.errno == errno.EEXIST and os.path.isdir(folder):
             pass
         else: raise

def safe_open_folder(path):
    create_folder(os.join) 

answer = urllib2.urlopen(baseurl)
print retrive_problem_ids(answer.read())

users = urllib2.urlopen(userurl)
print retrive_users(users.read())


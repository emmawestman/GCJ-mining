from downloadgcj import *
import sorting
from download_input import *
import os
import multiprocessing as mp
import time
import urllib2
from datetime import datetime
import sys
from functools import partial

# import own modules from diffrent directory

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from finding_regexes import *
from stuff_module import *
from write_to_csv import *

problem_ids = []

NUMBER_OF_PAGES = 3030


# not needed at the moment since competisions ids are selected
def get_all_contests_id():
	answer = urllib2.urlopen(get_BASE()).read()
	list_of_duplicates = filter_information('contest/[\d]+/dashboard','/',answer)
	return list(set(list_of_duplicates))

def retrive_problem_ids(url):
	page = urllib2.urlopen(url).read()
	#print "PAGE RESPONSE " + page
	return filter_information('\"id\":\s+\"\d+\"',':',page)

def build_base_url(contest_id):
   return get_BASE()+contest_id+'/scoreboard'

def retrive_token(contest_id):
	page = urllib2.urlopen(get_BASE()+contest_id+'/dashboard/do?cmd=GetInitialValues').read()
	token = filter_information('\"\w*=\"',None,page)[0]
	#print "TOKEN " + token
	return token



# removes outputfiles and similar files created by solutions
clean_home_dir()


#Pre processing stuff...
#list_of_contest_ids = get_all_contests_id()

list_of_contest_ids = get_CONTEST_IDS()

#Ask user how many contests to download
#number_of_contests = int(raw_input('Number of contests?'))
number_of_contests = len(list_of_contest_ids)



# Run the downloading function for downloding input

def download_input(contest_id):
	base_url = build_base_url(contest_id)
	PROBLEM_IDS =retrive_problem_ids(base_url)
	TOKEN = retrive_token(contest_id)
	download_all_input(contest_id, get_PROBLEM(), get_SIZE(), PROBLEM_IDS,TOKEN)


def download_input_serial():
	list_of_contest_ids = get_CONTEST_IDS()
	for x in list_of_contest_ids:
		download_input(x)

def download_input_mp():
	list_of_contest_ids = get_CONTEST_IDS()
	pool = mp.Pool(processes = NBR_OF_PROCESSES)
	results = pool.map(download_input,list_of_contest_ids)


# Run the downloading fucntion
#READ FROM INPUT FILE


def download_solutions_serial():
	list_of_contest_ids = get_CONTEST_IDS()
	list_of_pages = range(1,NUMBER_OF_PAGES+1,30)
	for contest_id in list_of_contest_ids:
		base_url = build_base_url(contest_id)
		problem_ids = retrive_problem_ids(base_url)
		for problem_id in problem_ids:
			for limit in list_of_pages:
				download_one_page(problem_id,contest_id,limit)
			


def download_solution_mp():
	list_of_contest_ids = get_CONTEST_IDS()
	pool = mp.Pool(processes = 6)
	for contest_id in list_of_contest_ids:
		problem_ids = retrive_problem_ids(build_base_url(contest_id))
		for problem_id in problem_ids:
			list_of_pages = range(1,NUMBER_OF_PAGES+1,30)
			first_func = partial(download_one_page,problem_id)
			partial_download_func = partial(first_func,contest_id)
			pool.map(partial_download_func,list_of_pages)

def download_table_data_mp():
	list_of_contest_ids = get_CONTEST_IDS()
	list_of_page_numbers_limit = [NUMBER_OF_PAGES] * len(list_of_contest_ids)
	pool2 = mp.Pool(processes = NBR_OF_PROCESSES)
	results = pool2.map(download_solution,zip(list_of_contest_ids,list_of_page_numbers_limit))







print 'Starting to sort all zip files...'
for problem_id in get_PROBLEM_IDS(gcj_path):
	print 'Sorting contest ' + problem_id
	dict = sorting.sort_files(problem_id)
	write_to_csv_file(problem_id+'.csv',dict)



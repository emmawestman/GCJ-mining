from downloadgcj import *
import sorting
from download_input import *
import os
import multiprocessing as mp
import time
import urllib2
from datetime import datetime
import sys

# import own modules from diffrent directory

gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from finding_regexes import *
from stuff_module import *

problem_ids = []

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
	pool = mp.Pool(processes = 6)
	results = pool.map(download_input,list_of_contest_ids)


# Run the downloading fucntion
#READ FROM INPUT FILE
def download_solution(contest_id):
	base_url = build_base_url(contest_id)
	problem_ids = retrive_problem_ids(base_url)
	with open (os.path.join(gcj_path,'p_ids.in'),'wb') as f :
		for problem_id in problem_ids:
			f.write(problem_id+'\n')
	download_all_pages(base_url,problem_ids,contest_id)


def download_solution_serial():
	list_of_contest_ids = get_CONTEST_IDS()
	for x in list_of_contest_ids:
		download_solution(x)

def download_solutions_mp():
	list_of_contest_ids = get_CONTEST_IDS() 
	pool2 = mp.Pool(processes = 6)
	results = pool2.map(download_solution,list_of_contest_ids)

download_input_mp()
download_solutions_mp()

print 'Sarting to sort all zip files...'
start = time.time()

for i in range(0,number_of_contests):
	CONTEST_ID = list_of_contest_ids[i]
	print 'Sorting contest ' + CONTEST_ID
	sorting.sort_files(CONTEST_ID)

end = time.time()
diff = end - start
write_to_log('Time for sorting all files: ', diff)









=======
#download_input_serial()
sorting.sort_files('5652388522229760',0)
#download_solution_serial()
'''
print 'Starting to sort all zip files...'
for problem_id in get_PROBLEM_IDS(gcj_path):
	for i in range(0,1):
		print 'Sorting contest ' + problem_id
		sorting.sort_files(problem_id,i)
'''		
>>>>>>> csv

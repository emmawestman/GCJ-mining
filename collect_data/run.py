from downloadgcj import *
import sorting
from download_input import *
import os
import multiprocessing as mp
import time
from finding_regexes import *
import urllib2
from datetime import datetime
import sys
from stuff_module import clean_home_dir


# import own modules from iffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *



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


def format_time(time):
	m = time / 60
	s = time % 60
	return str(m) + 'min ' + str(s) +'sec'

def write_to_log(message, time):
	completeName = os.path.join(get_HOME_PATH(), 'log.txt')         
	file1 = open(completeName, "a")
	now = str(datetime.now())
	message = now + " : " + message + format_time(time) + " \n"
	file1.write(message)
	file1.close()


def print_log_file():
	completeName = os.path.join(get_HOME_PATH(), 'log.txt')         
	file1 = open(completeName, "r")
	print file1.read()
	file1.close()

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
	start = time.time()
	print 'Downloading input contest ' + contest_id
	base_url = build_base_url(contest_id)
	PROBLEM_IDS =retrive_problem_ids(base_url)	
	TOKEN = retrive_token(contest_id)
	download_all_input(contest_id, get_PROBLEM(), get_SIZE(), PROBLEM_IDS,TOKEN)
	end = time.time()

print 'Downloading input files...'
pool = mp.Pool(processes = 6)
results = pool.map(download_input,list_of_contest_ids)

print 'Done downloing input files!'

#write_to_log('Time to download all input files to solutions: ', diff)


# Run the downloading fucntion
#READ FROM INPUT FILE 
def download_solution(contest_id):
	print 'Downloading solutions from GCJ...'
	start = time.time()
	base_url = build_base_url(contest_id)
	print 'Downloading contest ' + contest_id
	problem_ids =retrive_problem_ids(base_url)
	download_all_pages(base_url,problem_ids,contest_id)
	end = time.time()

print 'Downloading solutions from GCJ...'
pool2 = mp.Pool(processes = 6)
results = pool2.map(download_solution,list_of_contest_ids)


print 'Done downloading solutions!'
#end = time.time()
#diff = end - start
#write_to_log('Time to download all solutions: ', diff)



# Run the sorting function
# measure time to sort
'''
print 'Sarting to sort all zip files...'
start = time.time()

for i in range(0,number_of_contests):
	CONTEST_ID = list_of_contest_ids[i]
	print 'Sorting contest ' + CONTEST_ID
	sorting.sort_files(CONTEST_ID)

end = time.time()
diff = end - start
write_to_log('Time for sorting all files: ', diff)

'''











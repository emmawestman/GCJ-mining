import downloadgcj
import sorting
import download_input
import os
import time
from finding_regexes import *
import urllib2
from compilegcj import * 
home_path = os.path.join('..')


BASE = "https://code.google.com/codejam/contest/"

SIZE = ["-small.practice.in", "-large.practice.in"]

#CONTEST_ID = "6254486"

PROBLEM =['A', 'B', 'C', 'D', 'E'] 

LANGUAGE = ['java', 'C', 'C++', 'Python', 'C#']


def get_all_contests_id():
	answer = urllib2.urlopen(BASE).read()
	list_of_duplicates = filter_information('contest/[\d]+/dashboard','/',answer)
	return list(set(list_of_duplicates))

def retrive_problem_ids(url):
	page = urllib2.urlopen(url).read()
	#print "PAGE RESPONSE " + page
	return filter_information('\"id\":\s+\"\d+\"',':',page)

def build_base_url(contest_id):
   return BASE+contest_id+'/scoreboard'

def retrive_token(contest_id):
	page = urllib2.urlopen(BASE+contest_id+'/dashboard/do?cmd=GetInitialValues').read()
	token = filter_information('\"\w*=\"',None,page)[0]
	#print "TOKEN " + token	
	return tokenlist_of

def write_to_log(message, time):
	completeName = os.path.join(home_path, 'log.txt')         
	file1 = open(completeName, "a")
	file1.write(message + str(time) + 'sec \n')
	file1.close()

#Pre processing stuff...
list_of_contest_ids = get_all_contests_id()
print list_of_contest_ids

#Ask user how many contests to download
number_of_contests = int(raw_input('Number of contests?'))
'''
# Run the downloading function for downloding input
print 'Downloading input files...'
start = time.time()
for i in range(0,number_of_contests):
	CONTEST_ID = list_of_contest_ids[i]
	print 'Downloading contest ' + CONTEST_ID
	base_url = build_base_url(CONTEST_ID)
	PROBLEM_IDS =retrive_problem_ids(base_url)		
	TOKEN = retrive_token(CONTEST_ID)
	download_input.download_all_input(CONTEST_ID, PROBLEM, SIZE, PROBLEM_IDS,TOKEN)

end = time.time()

print 'Done downloing input files!'

diff = end - start
write_to_log('Time to download all input files to solutions: ', diff)



# Run the downloading fucntion
#READ FROM INPUT FILE 
print 'Downloading solutions from GCJ...'
start = time.time()
for cas in range(0,number_of_contests):
	contest_id = list_of_contest_ids[cas]
	base_url = build_base_url(CONTEST_ID)
	problem_ids =retrive_problem_ids(base_url)
	downloadgcj.download_all_pages(base_url,problem_ids,contest_id)

print 'Done downloading solutions!'
end = time.time()
diff = end - start
write_to_log('Time to download all solutions: ', diff)



# Run the sorting function
# measure time to sort
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
# Run the compile and run scripts on the downloaded files	
print 'Sarting to sort all zip files...'
start = time.time()

for i in range(0,number_of_contests):
	CONTEST_ID = list_of_contest_ids[i]
	for l in LANGUAGE:
		l_start = time.time()
		print 'Compile and Runs: ' + l + 'in contest: ' + CONTEST_ID
		a, b, c, d = compile_language(l, CONTEST_ID)
		l_end = time.time()
		l_diff = l_start -l_end
		write_to_log('Time to compile and run for '+ l +': ', l_diff)
		write_to_log(l + ': ' + str(a) + ' out of ' + str(b) + ' programs compiled sucessfully', 0)
		write_to_log(l + ': ' + str(c) + ' out of ' + str(d) + ' programs ran sucessfully', 0)

end = time.time()
diff = end - start
write_to_log('Time to compile and run all programs: ', diff)






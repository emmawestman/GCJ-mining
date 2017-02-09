import downloadgcj
import sorting
import download_input
import os
import time

home_path = os.path.join('..')

PATH = os.path.join('..','solutions_qualification_2016')

BASE = "https://code.google.com/codejam/contest/"

SIZE = ["-small.practice.in", "-large.practice.in"]

CONTEST_ID = "6254486"

PROBLEM =['A', 'B', 'C', 'D'] 

def retrive_problem_ids(url):
    page = urllib2.urlopen(url).read()
    return filter_information('\"id\":\s+\"\d+\"',':',page)

def build_base_url(contest_id):
   return BASE+contest_id+'/scoreboard'

def retrive_token(contest_id):
	page = urllib2.urlopen(BASE+contest_id+'/dashboard/do?cmd=GetInitialValues').read()
	return filter_information('\"csrf_middleware_token\":',page)[0]

def write_to_log(message, time):
	completeName = os.path.join(home_path, 'log.txt')         
	file1 = open(completeName, "a")
	file1.write(message + str(time) + 'sec \n')
	file1.close()

# Run the downloading function for downloding input
print 'Downloading input files...'
start = time.time()

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
number_of_contests = int(raw_input())
for cas in xrange(0,number_of_contests):
    contest_id = (raw_input())
    downloadgcj.download_all_pages(base_url,contest_id)

print 'Done downloading solutions!'
end = time.time()
diff = end - start
write_to_log('Time to download all solutions: ', diff)



# Run the sorting function
# measure time to sort
print 'Sarting to sort all zip files...'
start = time.time()
sorting.sort_files(PATH)
end = time.time()
diff = end - start
write_to_log('Time for sorting all files: ', diff)


	






''' sScript for downloadin the input files to run the solutions'''

import urllib2
import os

BASE = "https://code.google.com/codejam/contest/"

SIZE = ["-small.practice.in", "-large.practice.in"]

CONTEST_ID = "6254486"

PROBLEM =['A', 'B', 'C', 'D'] 

#PROBLEM_ID = "5652388522229760"

TOKEN = "NDU5YzFkMGU3OTk5ZjU5NWYxZjA1YjJlMGVkM2E4MjF8fDE0ODU4NjgyODI3NTUzMDA%3D"

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

def build_base_url(contest_id):
   return 'https://code.google.com/codejam/contest/'+contest_id+'/scoreboard'

def retrive_problem_ids(url):
    page = urllib2.urlopen(url).read()
    return filter_information("\"id\":",page)

base_url =  build_base_url(CONTEST_ID)

PROBLEM_IDS = retrive_problem_ids(base_url)
print PROBLEM_IDS





def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError:
         if os.path.exists(folder):
             pass
         else: 
             raise

#retrives the input file in constest c_id, for prob A/B/C/D, of size small/large
def retrive_input(c_id, prob, size, prob_id): 
	url = BASE + c_id + '/dashboard/do/' + prob + size +'?cmd=GetInputFile&problem=' + prob_id + '&input_id=1&filename=' + prob + size+'&redownload_last=1&agent=website&csrfmiddlewaretoken=' + TOKEN
	answer = urllib2.urlopen(url).read()
	'''if answer.startswith('Server Error'):
       	return
    else :'''
	path = os.path.join('..','input_qualification_2016')
	create_folder(path)
	os.chdir(path)	
	if size == "-small.practice.in":
		s = '0'
	else:
		s = '1'
	with open(prob_id + "_" + s + '.in', 'w') as f:
		f.write(answer)
     
def download_all_input(c_id, prob, size, prob_ids):
	i = 0
	for p in prob:
		for s in size:
			prob_id = prob_ids[i]
			retrive_input(c_id, p, s, prob_id)
		i += 1


#retrieve_solution_input(url_small)
#build_urls()

download_all_input(CONTEST_ID, PROBLEM, SIZE, PROBLEM_IDS)


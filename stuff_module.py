import os
import urllib2
import re
def build_base_url(contest_id):
   return 'https://code.google.com/codejam/contest/'+contest_id+'/scoreboard'


def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError:
         if os.path.exists(folder):
             pass
         else: 
             raise


def filter_information(regex,page):
    remaining_page = page
    ids = []
    while regex in remaining_page:
    	index = remaining_page.find(regex)
    	index += len(regex)
    	remaining_page = remaining_page[index:]
    	# finding the start qutation mark for problem id
    	start_index = remaining_page.find("\"")
    	# find the end qutation mark for problem id
    	end_index = remaining_page[start_index+1:].find("\"")
    	# extract problem id string
    	item = remaining_page[start_index+1:end_index+2]
    	ids.append(item)
    	remining_page = remaining_page[end_index+3:]
    return ids

def filter_information2(page):
	list_of_matches = []
	for match in re.findall(r'contest/[\d]+/dashboard',page): 
		list_of_matches.append(match.split('/')[1])
	return list_of_matches

def retrive_problem_ids(url):
    page = urllib2.urlopen(url).read()
    return filter_information("\"id\":",page)



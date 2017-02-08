'''Script for downloadin the input files to run the solutions'''

import urllib2
import os
from stuff_module import create_folder,build_base_url,filter_information, retrive_problem_ids

BASE = "https://code.google.com/codejam/contest/"

SIZE = ["-small.practice.in", "-large.practice.in"]

CONTEST_ID = "6254486"

PROBLEM =['A', 'B', 'C', 'D'] 


def retrive_token(contest_id):
	page = urllib2.urlopen('http://code.google.com/codejam/contest/'+contest_id+'/dashboard/do?cmd=GetInitialValues').read()
	return filter_information('\"csrf_middleware_token\":',page)[0]

#retrives the input file in constest c_id, for prob A/B/C/D, of size small/large
def retrive_input(c_id, prob, size, prob_id,token): 
	url = BASE + c_id + '/dashboard/do/' + prob + size +'?cmd=GetInputFile&problem=' + prob_id + '&input_id=1&filename=' + prob + size+'&redownload_last=1&agent=website&csrfmiddlewaretoken=' + token
	answer = urllib2.urlopen(url).read()
	print answer
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
     
def download_all_input(c_id, prob, size, prob_ids,token):
	i = 0
	for p in prob:
		for s in size:
			prob_id = prob_ids[i]
			retrive_input(c_id, p, s, prob_id,token)
		i += 1

'''Script for downloadin the input files to run the solutions'''

import urllib2
import os
from stuff_module import create_folder

BASE = "https://code.google.com/codejam/contest/"

SIZE = ["-small.practice.in", "-large.practice.in"]

CONTEST_ID = "6254486"

PROBLEM =['A', 'B', 'C', 'D','E'] 


#retrives the input file in constest c_id, for prob A/B/C/D, of size small/large
def retrive_input(c_id, prob, size, prob_id,token): 
	url = BASE + c_id + '/dashboard/do/' + prob + size +'?cmd=GetInputFile&problem=' + prob_id + '&input_id=1&filename=' + prob + size+'&redownload_last=1&agent=website&csrfmiddlewaretoken=' + token
	answer = urllib2.urlopen(url).read()
	#print answer
	'''if answer.startswith('Server Error'):
       	return
    else :'''
	path = os.path.join('..','input_' + c_id)
	create_folder(path)
	os.chdir(path)	
	if size == "-small.practice.in":
		s = '0'
	else:
		s = '1'
	with open(prob_id + "_" + s + '.in', 'w') as f:
		f.write(answer)
     
def download_all_input(c_id, prob, size, prob_ids,token):
	print prob_ids
	for x in range(0,len(prob_ids)):
		for s in size:
			print 'X IS ' + str(x)
			p = prob[x]
			prob_id = prob_ids[x]
			retrive_input(c_id, p, s, prob_id,token)


'''Script for downloadin the input files to run the solutions'''

import urllib2
import os
from stuff_module import create_folder
import sys

# import own modules from iffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *



#retrives the input file in constest c_id, for prob A/B/C/D, of size small/large
def retrive_input(c_id, prob, size, prob_id,token):
	if size == "-small.practice.in":
		s = '0'
	else:
		s = '1'
	url = get_BASE() + c_id + '/dashboard/do/' + prob + size +'?cmd=GetInputFile&problem=' + prob_id + '&input_id=' + s + '&filename=' + prob + size+'&redownload_last=1&agent=website&csrfmiddlewaretoken=' + token
	answer = urllib2.urlopen(url).read()
	path = os.path.join(get_HOME_PATH(),'datacollection','input')
	create_folder(path)
	with open(os.path.join(path,prob_id + "_" + s + '.in'), 'w') as f:
		f.write(answer)

def download_all_input(c_id, prob, size, prob_ids,token):
	print ['Problems ids: '] + prob_ids
	for x in range(0,len(prob_ids)):
		for s in size:
			p = prob[x]
			prob_id = prob_ids[x]
			retrive_input(c_id, p, s, prob_id,token)

import urllib2
import json
import os
import sys
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *
 
def build_table_url(contest_id,pos):
	return 'https://code.google.com/codejam/contest/'+contest_id+'/scoreboard/do/?cmd=GetScoreboard&contest_id='+contest_id+'&show_type=all&start_pos=' + str(pos)


def write_statistics_to_csv(statistics_dict,user_dict,contest_id):
	problem_ids = get_PROBLEM_IDS(gcj_path)
	for problem_id in problem_ids:
		write_to_csv_file(problem_id+'.csv', user_dict)
	write_to_csv_file(contest_id+'.csv', statistics_dict) 


def download_table_data(contest_id_and_limit):
	contest_id,limit= contest_id_and_limit
	statistics_dict = {}
	user_dict = {}
	for pos in range(1,limit+1,30):
		print "for loop"
		url = build_table_url(contest_id,pos)
		raw_data = urllib2.urlopen(url).read()
		json_data = json.loads(raw_data)
		for row in json_data['rows']:
			row_data_dict = {}
			row_data_dict['penalty'] = row['pen']
			row_data_dict['points'] = row['pts'] 
			user_dict[row['n']]= {}
			statistics_dict[row['n']]=row_data_dict	
	write_statistics_to_csv (statistics_dict,user_dict,contest_id)




	
download_table_data(('6254486',30))
	

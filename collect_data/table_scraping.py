import urllib2
import json

url = 'https://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetScoreboard&contest_id=6254486&show_type=all&start_pos=1'

def table_scraping(url):
	raw_data = urllib2.urlopen(url).read()
	json_data = json.loads(raw_data)
	for row in json_data['rows']:
		print row['n'] + row ['pen'] + row['pts']



table_scraping(url)
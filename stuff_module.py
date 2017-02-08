import urllib2
from finding_regexes import *


def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError:
         if os.path.exists(folder):
             pass
         else: 
             raise

def retrive_problem_ids(url):
    page = urllib2.urlopen(url).read()
    print page
    return filter_information('\"id\":\s+\"\d+\"',':',page)


def build_base_url(contest_id):
   return 'https://code.google.com/codejam/contest/'+contest_id+'/scoreboard'
'''Script for dowloading all solutions to Qualification Round 2016'''

import urllib2
import os
from lxml import etree
#import shutil


baseurl = "https://code.google.com/codejam/contest/6254486/scoreboard#vf=1"
exampleurl = "https://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetSourceCode&problem=5652388522229760&io_set_id=0&username=Lewin"

io_set_id_0 = "0";
io_set_id_1 = "1"

PROBLEM_A = '5652388522229760'
PROBLEM_B = '5634697451274240'
PROBLEM_C = '5738606668808192'
PROBLEM_D = '5636311922769920'

answer = urllib2.urlopen(baseurl)
s = answer.read()
html = etree.HTML(s)
print html

'''def retrieve_sol(problem,io_set_id,username):
    requesturl = 'https://code.google.com/codejam/contest/6254486/scoreboard/do/?cmd=GetSourceCode&problem='+
                  problem+'&io_set_id='+ io_set_id+'&username='username
    return urllib2.urlopen(reuqesturl)

def create_folder (folder):
    try:
        os.makedirs(path)
    except OSError as exs :
         if exc.errno = errno.EEXIST and os.path.isdir(path)
             pass
         else: raise

def safe_open_folder(path):
    create_folder(os.join) 
'''



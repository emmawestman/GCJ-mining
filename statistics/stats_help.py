import os
import pandas
import sys
import re
import urllib2  


gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from write_to_csv import *

C_ID_TIMELINE = ['Qualification Round 2016', 'Round 1A 2016', 'Round 1B 2016', 'Round 1C 2016', 'Qualification Round 2015', 'Round 1A 2015', 'Round 1B 2015', 'Round 1C 2015', 'Qualification Round 2014', 'Round 1A 2014', 'Round 1B 2014', 'Round 1C 2014', 'Qualification Round 2013', 'Round 1A 2013', 'Round 1B 2013', 'Round 1C 2013', 'Qualification Round 2012', 'Round 1A 2012', 'Round 1B 2012', 'Round 1C 2012']

def invert_dict(old_dict) :
    return {v: k for k, v in old_dict[c_id].iteritems()}

def get_cid_name_dict(key) :
    csv_df = pandas.read_csv(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'cid_name_map.csv'))
    csv_df.set_index(key, drop=True, inplace=True)
    return csv_df.to_dict(orient="index")

def CIDS_timeline_order() :
    name_cid_dict = get_cid_name_dict('name')
    cids_in_time_order = []
    i = len(C_ID_TIMELINE)-1
    for idx,name in enumerate(C_ID_TIMELINE) :
        name = C_ID_TIMELINE[i-idx]
        c_id = name_cid_dict[name]
        cids_in_time_order.append(str(c_id['c_id']))
    return cids_in_time_order

def get_pid_name_dict():
    csv_df = pandas.read_csv(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'pid_name_map.csv'))
    csv_df.set_index('p_id', drop=True, inplace=True)
    return csv_df.to_dict(orient="index")

def create_cid_name_map() :
    cids = get_CONTEST_IDS()
    just_names = []
    for c_id in cids:
        url = get_BASE()+c_id+'/scoreboard'
        page = urllib2.urlopen(url).read()
        names = re.findall('name = \"(.*)\"',page)
        just_names.append(names[1])

    filename = os.path.join(get_HOME_PATH(), 'GCJ-backup', 'cid_name_map.csv')
    print cids
    print just_names
    df = pandas.DataFrame(just_names, columns=['name'], index=cids)
    df.index.name = 'c_id'
    print df
    df.to_csv(filename)

def create_pid_name_map() :
    cids = CIDS_timeline_order()
    pid_name_dict = {}
    for c_id in cids:
        url = get_BASE()+c_id+'/scoreboard'
        page = urllib2.urlopen(url).read()
        pids = re.findall('\"id\": \"(.+)\"',page)
        names = re.findall('\"title\": \"(.+)\"',page)
        for idx, pid in enumerate(pids) :
            name_dict = {'name' : names[idx]}
            pid_name_dict[pid] = name_dict
    filename = os.path.join(get_HOME_PATH(), 'GCJ-backup', 'pid_name_map.csv')
    df = pandas.DataFrame(pid_name_dict)
    df.index.name = 'p_id'
    print df
    df.to_csv(filename)

def get_name_of_pid(pid):
    dict = get_pid_name_dict()
    pid_name_dict = dict['name']
    return pid_name_dict[pid]

    



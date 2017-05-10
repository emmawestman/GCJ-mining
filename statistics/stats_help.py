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

def init_dict() :
    return {'Java': 0.0, 'Python': 0.0, 'C': 0.0, 'C++': 0.0, 'C#': 0.0}

def invert_dict(old_dict) :
    return {v: k for k, v in old_dict[c_id].iteritems()}

def get_cid_name_dict(key) :
    csv_df = pandas.read_csv(os.path.join(get_HOME_PATH(), 'GCJ-backup', 'cid_name_map.csv'))
    csv_df.set_index(key, drop=True, inplace=True)
    return csv_df.to_dict(orient="index")

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
    all_pids = []
    all_names = []
    all_leters = []
    for c_id in cids:
        url = get_BASE()+c_id+'/scoreboard'
        page = urllib2.urlopen(url).read()
        pids = re.findall('\"id\": \"(.+)\"',page)
        names = re.findall('\"title\": \"(.+)\"',page)
        for name in  names :
            all_names.append(''.join(list(name[3:])))
            all_leters.append(''.join(list(name[:1])))
        all_pids += pids
    filename = os.path.join(get_HOME_PATH(), 'GCJ-backup', 'pid_name_map.csv')
    df = pandas.DataFrame( {'p_id': all_pids, 'name': all_names, 'letter': all_leters})
    print df
    df.to_csv(filename)

def get_column_of_pid(pid, column):
    split = pid.split('_') #contoains pid as first elem and 0/1 as second
    pid = int(split[0])
    dict = get_pid_name_dict()
    pid_name_dict = dict[pid]
    return pid_name_dict[column] + '_' + split[1]

def get_name_of_pid(pid):
    return get_column_of_pid(pid, 'name')

def get_letter_of_pid(pid):
    return get_column_of_pid(pid, 'letter')

def get_name_of_cid(cid):
    dict = get_cid_name_dict('c_id')
    cid_dict = dict[cid]
    return cid_dict['name']

def CIDS_name_timeline_order() :
    names_in_time_order = []
    for cid in get_CONTEST_IDS() :
        names_in_time_order.append(get_name_of_cid(int(cid)))
    return names_in_time_order


# kanske inte blir i odning... har inte testat
def PIDS_name_timeline_order(pids) :
    names = []
    for pid in pids:
        name = get_name_of_pid(pid)
        if str(pid).endswith('0'):
            name +=' - Small'
        else :
            name += ' - Large'
    names.append(name)


def PIDS_letter_timeline_order(pids) :
    letters = []
    for pid in pids:
        letter = get_letter_of_pid(pid)
        if str(pid).endswith('0'):
            letter += '_0'
        else :
            letter += '_1'
    letters.append(letter)

def filter_dummyvalues(data,error_column):
    data = data.loc[data[error_column] != '-']
    data = data.loc[data[error_column] != 0]
    data = data.loc[data[error_column] != '0']
    data = data.loc[data[error_column] != -1]
    data = data.loc[data[error_column] != '-1']
    data = data.apply(pandas.to_numeric, errors='ignore')
    return data

# takes  list of columns as argument
def get_all_data(columns) :
    data = pd.DataFrame()
    p_ids = get_PROBLEM_IDS(os.path.join('../'))
    for p_id in p_ids:
        #print p_id
        path = os.path.join('../..', 'GCJ-backup', p_id+'.csv')
        df = pd.read_csv(path)
        try:
            df = df[columns]
            df['problem_id'] = p_id
            data = data.append(df)

        except KeyError:
            #df = df['language']
            #size = len(df.index)
            #for c in columns:
                #df[c] = ['-']*size
            print 'skiped: ' + p_id


    return data

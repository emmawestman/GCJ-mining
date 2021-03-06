import os

# all selceted contest ids


CONTEST_IDS = ['6254486','4304486' ,'11254486', '4314486', '6224486', '4224486', '8224486', '4244486', '2974486', '2984486', '2994486','3004486', '2270488', '2418487', '2434486', '2437488', '1460488', '1645485', '1836486', '1781488']

LANGUAGE = ['Java', 'C', 'C++', 'Python', 'C#']


PROBLEM =['A', 'B', 'C', 'D', 'E']

#turkos, pink, blue, grey, purple
COLORS = ['#4B9E86', '#B52D8E','#6842D1', '#1A6D89', '#D88A65']

# get the folder above the git repo from collect_data folder
HOME_PATH = os.path.join('../../')




SIZE = ["-small.practice.in", "-large.practice.in"]
BASE = "https://code.google.com/codejam/contest/"

def get_COLORS() :
    return COLORS

def get_CONTEST_IDS() :
    return CONTEST_IDS

def get_LANGUAGE() :
    return LANGUAGE

def get_PROBLEM() :
    return PROBLEM

def get_HOME_PATH() :
    return HOME_PATH

def get_GCJ_BACKUP_PATH():
	return os.path.join(get_HOME_PATH(), 'GCJ-backup')


def get_SIZE() :
    return SIZE

def get_BASE() :
    return BASE

PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(), 'datacollection', 'input'))

def get_INPUT_PATH() :
    return PATH_INPUT

#get all ids wich have small and larrge input
def get_PROBLEM_IDS_BOTH(gcj_path):
	with open (os.path.join(gcj_path,'p_ids.in'),'rb') as content :
		p_ids = content.read().split('\n')
		p_ids = p_ids [:len(p_ids)-1]
		ret_list = []
		for p_id in p_ids :
			if len (p_id) > 0 :
				if not (p_id == '5756407898963968' or p_id == '5752104073297920' or p_id == '1483485') :
					ret_list.append(p_id)
	return ret_list

def get_PROBLEM_IDS(gcj_path):
	with open (os.path.join(gcj_path,'p_ids.in'),'rb') as content :
		p_ids = content.read().split('\n')
		p_ids = p_ids [:len(p_ids)-1]
		ret_list = []
		for p_id in p_ids :
			if len (p_id) > 0 :
				if p_id == '5756407898963968' or p_id == '5752104073297920' or p_id == '1483485' :
					range = [0]
				else:	
					range = [0,1]
				for i in range :
					ret_list.append(p_id+'_'+str(i))
	return ret_list

def get_PROBLEM_IDS_CONTEST(p_ids):
	ret_list = []
	for p_id in p_ids :
		if len (p_id) > 0 :
			if p_id == '5756407898963968' or p_id == '5752104073297920' or p_id == '1483485' :
				range = [0]
			else:	
				range = [0,1]
			for i in range :
				ret_list.append(p_id+'_'+str(i))
	return ret_list



def get_FILE_ENDING(lang):
    if lang == 'java':
        return ['.java']
    elif lang == 'Python':
        return ['.py']
    elif lang == 'C' :
        return ['.c']
    elif lang == 'C#' :
        return ['.cs']
    elif lang == 'C++' :
        return ['.cpp', '.C', '.cc', '.CPP', '.c++', '.cp', '.cxx']
    else :
        print 'Not a valid language'

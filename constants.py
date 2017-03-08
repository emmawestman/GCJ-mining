import os

# all selceted contest ids

CONTEST_IDS = ['6254486','4304486', '11254486', '4314486', '6224486', '4224486', '8224486', '4244486', '2974486', '2984486', '2994486',
'3004486', '2270488', '2418487', '2434486', '2437488', '1460488', '1645485', '1836486', '1781488']

# contest on emmas computer
#['1128486', '2984486']
LANGUAGE = ['java', 'C', 'C++', 'Python', 'C#']

PROBLEM =['A', 'B', 'C', 'D', 'E']

# get the folder above the git repo from collect_data folder
HOME_PATH = os.path.join('../../')


BASE = "https://code.google.com/codejam/contest/"

SIZE = ["-small.practice.in", "-large.practice.in"]

BASE = "https://code.google.com/codejam/contest/"



def get_CONTEST_IDS() :
	return CONTEST_IDS

def get_LANGUAGE() :
	return LANGUAGE

def get_PROBLEM() :
	return PROBLEM

def get_HOME_PATH() :
	return HOME_PATH

def get_SIZE() :
	return SIZE

def get_BASE() :
	return BASE


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

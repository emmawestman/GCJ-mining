import os
import pandas
from constants import *



def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError:
         if os.path.exists(folder):
             pass
         else:
             raise

def clean_home_dir(path):
	files = os.listdir(path)
	all_files = [ f for f in files if os.path.isfile(f) ]
	to_remove = [ f for f in all_files if not(f.endswith('.py')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.in')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.h')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.gitignore')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.git')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('README.txt')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('errors.txt')) ]
	for f in to_remove:
		print 'removed file: ' + f
		os.remove(f)



def renamejavaToJava():
    list_of_problem_ids = get_PROBLEM_IDS(os.getcwd())
    for p_id in list_of_problem_ids:
        path_to_csv = os.path.realpath(os.path.join(os.getcwd(),'../','GCJ-backup',p_id+'.csv'))
        problem_df = pandas.read_csv(path_to_csv)
        problem_df['language'].replace('java','Java',inplace = True)
        problem_df.to_csv(path_to_csv,index=False)

renamejavaToJava()

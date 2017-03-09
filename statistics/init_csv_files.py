import csv
import os
import sys
from write_to_csv import *

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *

def run_init() :
    for p_id in get_PROBLEM_IDS(gcj_path) :
        dict = init_csv(p_id)
        create_init_csv(p_id, dict)

run_init()


import csv
import os
import sys
from write_to_csv import *

# import own modules from diffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *

def run_init() :
    for c_id in get_CONTEST_IDS() :
        dict = init_csv(c_id)
        create_init_csv(c_id, dict)

run_init()

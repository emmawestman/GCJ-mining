import sys
import os
gcj_path = os.path.join(os.getcwd(), 'collect_data/')
sys.path.insert(0, gcj_path)
from run import *

gcj_path = os.path.join(os.getcwd(), 'statistics/')
sys.path.insert(0, gcj_path)
from cloc import *

gcj_path = os.path.join(os.getcwd(), 'compile/')
sys.path.insert(0, gcj_path)
from compilegcj import *

master_do_all_stuff()
cloc_all()
compile_all()

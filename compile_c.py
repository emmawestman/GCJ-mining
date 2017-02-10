import os
import subprocess
from compile_support_module import *

PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))

	
def compile_c(path):
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			print 'compiling file nbr: ' + str(nbr_of_files)
			
			user, filename = get_compile_info('C', root, f)

			cmd = ['g++ ' + os.path.join(root,f) + ' -o ' + os.path.join(root,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				print 'failed to run problem: ' + root
				print errors
			else:
				succes_nbr += 1
	return succes_nbr, nbr_of_files


def run_c(path):
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):	
		# only try to run the executable 
		filelist = [f for f in files if '.' not in f]
		for f in filelist:
			nbr_of_files += 1
			print 'running file nbr: ' + str(nbr_of_files)
			
			user, input_file = get_run_info('C', root)
		
			cmd = [os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT, input_file)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				print 'Error Running problem: ' + root
				#print errors

			else:
				succes_nbr += 1
	return succes_nbr, nbr_of_files



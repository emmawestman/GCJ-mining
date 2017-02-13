import os
import subprocess
from compile_support_module import *

def compile_cpp(c_id):
	path = os.path.realpath(os.path.join('..','solutions_' + c_id, 'C++' ))
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	print path
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			print 'compiling c++ file nbr: ' + str(nbr_of_files)
			
			user, filename = get_compile_info('C++', root, f)

			cmd = ['g++ ' + os.path.join(root,f) + ' -o ' + os.path.join(root,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				#try with c++ 11 instead
				cmd = ['g++ -std=c++0x ' + os.path.join(root,f) + ' -o ' + filename]
				p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output, errors = p.communicate()
				if len(errors) > 0:
					print 'failed to run problem with g++11: ' + filename + ', for user: ' + user
					print errors
				else:
					succes_nbr +=1
			else:
				succes_nbr += 1
	return succes_nbr, nbr_of_files


def run_cpp(c_id):
	path = os.path.realpath(os.path.join('..','solutions_' + c_id, 'C++' ))
	PATH_INPUT = os.path.realpath(os.path.join('..','input_' + c_id))
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):	
		# only try to run the executable 
		filelist = [f for f in files if '.' not in f]
		for f in filelist:
			nbr_of_files += 1
			print 'running c ++ file nbr: ' + str(nbr_of_files)
			
			user, input_file = get_run_info('C++', root)
		
			cmd = [os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,input_file)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				print 'Error Running problem: ' + root
				#print errors

			else:
				succes_nbr += 1
	return succes_nbr, nbr_of_files



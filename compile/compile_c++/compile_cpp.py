import os
import subprocess
import sys

# import own modules from diffretn directory
compile_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, compile_path)
from compile_support_module import *

gcj_path = os.path.join(os.getcwd(), '../../')
sys.path.insert(0, gcj_path)
from constants import *

def copile_one_cpp_file(cmd):
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	exit_code = p.returncode
	return errors, exit_code

def compile_cpp(c_id, dict):
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C++' ))
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	print path

	file1 = open('cpp_errors.txt', "a")
	file1.write(path + '\n')
	for root, dirs, files in os.walk(path):
		for f in files if has_valid_file_ending('C', f):
			nbr_of_files += 1
			print 'compiling c++ file nbr: ' + str(nbr_of_files)
			
			user, filename = get_compile_info('C++', root, f)
			cmd = ['timeout 30s g++ -std=c++0x ' + os.path.join(root,f) + ' -o ' + os.path.join(root,filename)]
  			errors, exit_code = copile_one_cpp_file(cmd)
  			# update user dict
			user_id = get_user_id(os.path.join(root,f))
			user_dict = dict[user_id]
			user_dict['compiler_version'] = '-'
			# no timeout
			if int(exit_code) == 0:
				# an error occured
				if len(errors) > 0 and 'warning' not in errors:
					print 'Error in file: ' + os.path.join(root,f)
					print errors
					user_dict['compiled'] = 'NO'
	

				else:
					print 'success!'
					succes_nbr += 1
					user_dict['compiled'] = 'YES'
			else :
				print 'Timeout for file: ' + os.path.join(root,f)
				user_dict['compiled'] = 'NO'
				
				
	return succes_nbr, nbr_of_files, dict



def run_one_cpp_file(cmd):
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = p.communicate()
	exit_code = p.returncode
	return errors, exit_code

def run_cpp(c_id):
	path = os.path.realpath(os.path.join(get_HOME_PATH(),'solutions_' + c_id, 'C++' ))
	PATH_INPUT = os.path.realpath(os.path.join(get_HOME_PATH(),'input_' + c_id))
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):	
		# only try to run the executable 
		filelist = [f for f in files if '.' not in f]
		for f in filelist:
			nbr_of_files += 1
			print 'running c ++ file nbr: ' + str(nbr_of_files)
			
			user, input_file = get_run_info('C++', root)
		
			cmd = ['timeout 30s ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,input_file)]
  			errors, exit_code = run_one_cpp_file(cmd)
			# no timeout
			if int(exit_code) == 0:
				# a runtime error occured
				if len(errors) > 0:
					print 'Error Running problem: ' + root
					print errors
					file1 = open('cpp_run_errors.txt', "a")
					file1.write(path + '\n')
					file1.write(errors + '\n')
					file1.close()

				else:
					print 'success!'
					succes_nbr += 1
			else :
				print 'Timedout Running problem: ' + root
				file1 = open('cpp_run_errors.txt', "a")
				file1.write(path + '\n')
				file1.write('timedout' + '\n')
				file1.close()

	return succes_nbr, nbr_of_files



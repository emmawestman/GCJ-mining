import os
import subprocess
from compile_support_module import *

PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))

def compile_python(path):
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):
		nbr_of_files += 1
		for f in files:
			regexp = "/Python/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			filename = filename[:index]
			
			filename = filename + '.in'
			
			cmd = ['python ' + os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				print 'Running problem: ' + filename + ', for user: ' + user
				print errors
			else:
				succes_nbr += 1
	return succes_nbr, nbr_of_files

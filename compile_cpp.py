import os
import subprocess

PATH_INPUT = os.path.realpath(os.path.join('..','input_qualification_2016'))

'''
def compile_cpp2(path):
	nbr_of_files = 0
	succes_nbr = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			if (f.endswith(".cpp") or f.endswith(".cc") or f.endswith(".CPP") or f.endswith(".c++") or f.endswith(".cp") or f.endswith(".cxx")):
				try:
					subprocess.check_call(['g++', os.path.join(root,f), '-o', os.path.join(root,f) ]) # remove ending in f at last argumet
				except subprocess.CallProcessError:
					pass
				succes_nbr += 1
	return succes_nbr, nbr_of_files'''

def compile_cpp(path):
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	print path
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			print 'file nbr: ' + str(nbr_of_files)
			regexp = "/C++/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			index = f.find('.')
			name = f[:index]

			cmd = ['g++ ' + os.path.join(root,f) + ' -o ' + os.path.join(root,name)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				#try with c++ 11 instead
				cmd = ['g++ -std=c++0x ' + os.path.join(root,f) + ' -o ' + name]
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


def run_cpp(path):
	succes_nbr = 0
	nbr_of_files = 0
	for root, dirs, files in os.walk(path):	
		# only try to run the executable files
		filelist = [f for f in files if '.' not in f]
		for f in filelist:
			print f
			nbr_of_files += 1
			regexp = "/C++/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			filename = filename[:index]	
			filename = filename + '.in'

		
			cmd = [os.path.join(root,f) + ' < ' + os.path.join(PATH_INPUT,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				print 'Running problem: ' + filename + ', for user: ' + user
				print errors
			else:
				succes_nbr += 1
				#print 'Successfully compiled!'
	return succes_nbr, nbr_of_files



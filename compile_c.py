import os
import subprocess



def compile_c(path):
	#number of files that successfylly compiles
	succes_nbr = 0
	nbr_of_files = 0
	print path
	for root, dirs, files in os.walk(path):
		for f in files:
			nbr_of_files += 1
			regexp = "/C/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			filename = filename[:index]	
			filename = filename + '.in'
			# name without file ending
			index = f.find('.')
			name = f[:index]

			
			cmd = ['g++ ' + os.path.join(root,f) + ' -o ' + 'name']
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				# try with c++ 11 instead
				cmd = ['g++ -std=c++11' + os.path.join(root,f) + ' -o ' + 'name']
				if len(errors) > 0:
					print 'Running problem: ' + filename + ', for user: ' + user
					print errors
				else:
					succes_nbr +=1
			else:
				succes_nbr += 1
	return succes_nbr, nbr_of_files


def run_c(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			regexp = "/C/"
			index = root.find(regexp)
			filename = root[index+len(regexp):]
			index = filename.find('/')
			user = filename[index+1:]
			filename = filename[:index]
			print 'Running problem: ' + filename + ', for user: ' + user
			filename = filename + '.in'
			# name without file ending
			index = f.find('.')
			name = f[:index]

			
			cmd = ['./' + os.path.join(root,name) + ' < ' + os.path.join(PATH_INPUT,filename)]
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, errors = p.communicate()
			if len(errors) > 0:
				print errors
			else:
				print 'Successfully compiled!'



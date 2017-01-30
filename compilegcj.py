import os
import subprocess

PATH = os.path.join('..','solutions_qualification_2016','java')


def compile_java():
	for root, dirs, files in os.walk(PATH):
		for f in files:
						
			#proc = subprocess.Popen(cmd, shell=True, stdout=subproces.PIPE, stderr=subprocess.PIPE)
			#out, err = proc.communicate()
 			#print(out)
 			#print(err) 

compile_java()

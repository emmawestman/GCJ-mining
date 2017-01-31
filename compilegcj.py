import os
import subprocess

PATH = os.path.join('..','solutions_qualification_2016','java')


def compile_java():
	for root, dirs, files in os.walk(PATH):
		for f in files:
			subprocess.check_call(['javac', os.path.join(root,f) ])



def remove_class_files():
	for root, dirs, files in os.walk(PATH):
		filelist = [ f for f in files if (f.endswith(".class") or f.endswith(".txt") or f.endswith(".py~")) ]
		for f in filelist:			
			os.remove(os.path.join(root,f))
		

remove_class_files()
compile_java()

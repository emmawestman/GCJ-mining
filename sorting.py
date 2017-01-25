import os
import downloadgcj
import zipfile

PATH = os.path.join('..','solutions_qualification_2016')

def select_folder(filename):
	language = ""
	if filename == '.java':
		language = 'java' 
	elif filename == '.c':
		language = 'C'
	elif filename == ".cpp":
		language = 'C++'
	elif filename == '.cs':
		language = 'C#'
	elif filename == '.py':
		language = 'Python'
	else: 
		print "This is not one of the examined languages, this is: " + file_ending
	return os.path.join(PATH, language)

def get_file_ending(filename):
	index = filename.find(".")
	return filename[index:]


def sort_files(path):
	# create new folders for languages
	java_path = os.path.join(PATH, 'java')
	downloadgcj.create_folder(java_path)
	
	c_path = os.path.join(PATH, 'C')
	downloadgcj.create_folder(c_path)

	cpp_path = os.path.join(PATH, 'C++')
	downloadgcj.create_folder(cpp_path)

	cs_path = os.path.join(PATH, 'C#')
	downloadgcj.create_folder(cs_path)

	python_path = os.path.join(PATH, 'Python')
	downloadgcj.create_folder(python_path)
	
	# make a list of all files in the directory
	all_zip_names = os.listdir(PATH)
	#os.chdir(PATH)
	#all_zip_files = zipfile.ZipFile.namelist()	
	
	zip_filename = all_zip_names[0]
	print zip_filename
	#for filename in all_zip_names:
	#zip = zipfile.ZipFile(os.path.join(PATH, filename))
	
	# get the filename of file in the directory
	filename = zipfile.ZipFile(os.path.join(PATH, zip_filename)).namelist()[0]
	file_ending = get_file_ending(filename)
	print file_ending
	# extract file into this destination i.e. the correct language folder
	dest = select_folder(file_ending)
	print dest
	zipfile.ZipFile(os.path.join(PATH, zip_filename)).extractall(dest)






print sort_files(PATH)
#print get_file_ending("sheep.java")










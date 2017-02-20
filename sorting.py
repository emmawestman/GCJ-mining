import os
import downloadgcj
import zipfile




def select_folder(filename, path):
	language = ""
	if filename == '.java':
		language = 'java' 
	elif filename == '.c':
		language = 'C'
	elif filename == ".cpp" or filename == ".C" or filename == ".cc" or filename == ".CPP" or filename == ".c++" or filename == ".cp" or filename == ".cxx":
		language = 'C++' 
	elif filename == '.cs':
		language = 'C#'
	elif filename == '.py':
		language = 'Python'
	else: 
		print "This is not one of the examined languages, this is: " + filename
		# TODO remove this zip-file?
		return -1
	return os.path.join(path, language)

def get_file_ending(filename):
	index = filename.find(".")
	return filename[index:]


def get_info(filename):
	index = filename.find("_")
	return filename[:index], filename[index+1:]

def get_zip_files(files):
	zip_files = []
	for f in files:
		if f.endswith('_0') or f.endswith('_1'):
			zip_files.append(f)
	return zip_files



def sort_files(c_id):
	PATH = os.path.join('..','solutions_' + c_id)
	# make a list of all files in the directory
	all_zip_names = os.listdir(PATH)

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
	
	all_zip_names = get_zip_files(all_zip_names)
	for zip_filename in all_zip_names: 
		for filename in zipfile.ZipFile(os.path.join(PATH, zip_filename)).namelist():
			file_ending = get_file_ending(filename)
			print file_ending

			# extract file into this destination i.e. the correct language folder, problem id and username
			username, prob_id = get_info(zip_filename)
			#print username
			#print prob_id
			print 'Sorting ' + prob_id + ' for user: ' + username + 'into ' + file_ending 
			# language folder
			dest = select_folder(file_ending, PATH)
			''' check that the language is valid'''
			if dest != -1:
				# problem folder
				dest = os.path.join(dest, prob_id)
				downloadgcj.create_folder(dest)
				# username folder
				dest = os.path.join(dest, username)
				downloadgcj.create_folder(dest)
				#print dest	
				zipfile.ZipFile(os.path.join(PATH, zip_filename)).extract(filename,dest)

		#clean up, remove zip-file
		
		os.remove(os.path.join(PATH, zip_filename))
	print "Done sorting all zip files!"
















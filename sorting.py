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
	return os.path.join(PATH, language)

def get_file_ending(filename):
	index = filename.find(".")
	return filename[index:]


def get_info(filename):
	index = filename.find("_")
	return filename[:index], filename[index+1:]



def sort_files(path):
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
	
	for zip_filename in all_zip_names: 

		# only try to sort files that are zip files
		if zipfile.is_zipfile(zip_filename):
			#zip_filename = all_zip_names[0]
			print zip_filename
		
			# get the filename of file in the directory, now we assume the solution only consist of one fiel... thus 0
			for filename in zipfile.ZipFile(os.path.join(PATH, zip_filename)).namelist():
				file_ending = get_file_ending(filename)
				print file_ending

				# extract file into this destination i.e. the correct language folder, problem id and username
				username, prob_id = get_info(zip_filename)
				print username
				print prob_id
				# language folder
				dest = select_folder(file_ending)
				''' check that the language is valid'''
				if dest != -1:
					# problem folder
					dest = os.path.join(dest, prob_id)
					downloadgcj.create_folder(dest)
					# username folder
					dest = os.path.join(dest, username)
					downloadgcj.create_folder(dest)
					print dest
					zipfile.ZipFile(os.path.join(PATH, zip_filename)).extract(filename,dest)

			#clean up, remove zip-file
		
			os.remove(os.path.join(PATH, zip_filename))
	print "Done sorting all zip files!"
















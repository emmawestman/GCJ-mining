import os
import downloadgcj
import zipfile
import sys

# import own modules from iffrent directory
gcj_path = os.path.join(os.getcwd(), '../')
sys.path.insert(0, gcj_path)
from constants import *
from stuff_module import *



def select_folder(filename, path):
<<<<<<< HEAD
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
=======
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
		return -1,-1
	return os.path.join(path, language),language
>>>>>>> csv2

def get_file_ending(filename):
    index = filename.find(".")
    return filename[index:]


def get_info(filename):
    index = filename.find("_")
    return filename[:index], filename[index+1:]

def get_zip_files(files,PATH):
    retfiles = []
    for file in files :
        if not os.path.isdir(os.path.join(PATH,file)):
            retfiles.append(file)
    return retfiles

def comparingFunction(f):
    return not os.path.isdir(os.path.join(PATH,f));

def find_dest(file_names_list,PATH) :
    dest = -1
    for file_name in file_names_list :
        file_ending = get_file_ending(file_name)
        try_dest = select_folder(file_ending, PATH)
        if not try_dest == -1 :
            dest = try_dest
    return dest


def sort_files(p_id):
<<<<<<< HEAD
    PATH = os.path.join(get_HOME_PATH(),'solutions_' + p_id)
    # make a list of all files in the directory
    all_zip_names = os.listdir(PATH)

    # create new folders for languages
    java_path = os.path.join(PATH, 'java')
    create_folder(java_path)

    c_path = os.path.join(PATH, 'C')
    create_folder(c_path)

    cpp_path = os.path.join(PATH, 'C++')
    create_folder(cpp_path)

    cs_path = os.path.join(PATH, 'C#')
    create_folder(cs_path)

    python_path = os.path.join(PATH, 'Python')
    create_folder(python_path)

    all_zip_names = get_zip_files(all_zip_names,PATH)
    print all_zip_names
    for username in all_zip_names:
        file_names_list = zipfile.ZipFile(os.path.join(PATH, username)).namelist()
        # find corerct language
        dest = find_dest(file_names_list,PATH)
        if not dest == -1 :
            # create folder
            dest = os.path.join(dest, username)
            downloadgcj.create_folder(dest)

            for filename in file_names_list:
                print 'Sorting ' + p_id + ' for user: ' + username + ' into ' + dest
                # unpack files into folder
                zipfile.ZipFile(os.path.join(PATH, username)).extract(filename,dest)

        #clean up, remove zip-file
        os.remove(os.path.join(PATH, username))
    print "Done sorting all zip files!"

sort_files('5658068650033152_1')


=======
	PATH = os.path.join(get_HOME_PATH(),'datacollection','solutions_' + p_id)
	dict = {}
	# make a list of all files in the directory
	all_zip_names = os.listdir(PATH)

	# create new folders for languages
	java_path = os.path.join(PATH, 'java')
	create_folder(java_path)

	c_path = os.path.join(PATH, 'C')
	create_folder(c_path)

	cpp_path = os.path.join(PATH, 'C++')
	create_folder(cpp_path)

	cs_path = os.path.join(PATH, 'C#')
	create_folder(cs_path)

	python_path = os.path.join(PATH, 'Python')
	create_folder(python_path)

	all_zip_names = get_zip_files(all_zip_names,PATH)
	print all_zip_names
	for username in all_zip_names:
		print zipfile.ZipFile(os.path.join(PATH, username)).namelist()
		for filename in zipfile.ZipFile(os.path.join(PATH, username)).namelist():
			file_ending = get_file_ending(filename)
			print file_ending

			# extract file into this destination i.e. the correct language folder, problem id and username
			#username, prob_id = get_info(zip_filename)
			print 'Sorting ' + p_id + ' for user: ' + username + ' into ' + file_ending
			# language folder
			dest,language = select_folder(file_ending, PATH)
			''' check that the language is valid'''
			if dest != -1:
				# username folder 
				dest = os.path.join(dest, username)
				dict[username]={}
				user_dict =dict[username] 				
				user_dict['language']= language
				downloadgcj.create_folder(dest)
				#print dest
				zipfile.ZipFile(os.path.join(PATH, username)).extract(filename,dest)
		#clean up, remove zip-file

		os.remove(os.path.join(PATH, username))
	print "Done sorting all zip files!"
	return dict
>>>>>>> csv2

import os



def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError:
         if os.path.exists(folder):
             pass
         else: 
             raise

def clean_home_dir():
	files = os.listdir(os.getcwd())
	all_files = [ f for f in files if os.path.isfile(f) ]
	to_remove = [ f for f in all_files if not(f.endswith('.py')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.in')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.h')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.gitignore')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('.git')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('README.txt')) ]
	to_remove = [ f for f in to_remove if not(f.endswith('errors.txt')) ]
	for f in files_to_remove:
		print 'removed file: ' + f
		os.remove(f)


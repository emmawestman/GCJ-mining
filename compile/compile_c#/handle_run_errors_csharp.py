

def remove_files_in_a_user_solution(root):
	files = os.listdir(root)
	filelist = [ f for f in files if (f == 'TestMain.cs' or f.endswith('.exe')) ]
	for file in filelist:			
		os.remove(os.path.join(root,file))

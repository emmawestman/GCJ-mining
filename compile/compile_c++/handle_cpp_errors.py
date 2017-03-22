# Error handling for c++
import os
    

def replace_void_in_main(user_path, f) :
	file = open(os.path.join(user_path, f),'rb')
	content = file.readlines()
	file.close
 	for idx, line in enumerate(content) :
		if 'void main' in line :
			line.replace('void', '')
			content[idx] = line
			break
	content = '\n'.join(content)
	file = open(os.path.join(user_path, f),'wb') 
	file.write(content)  
	file.close()

def add_int_to_main(user_path, f) :
	file = open(os.path.join(user_path, f),'rb')
	content = file.readlines()
	file.close
 	for idx, line in enumerate(content) :
		if 'main' in line :
			line = 'int ' + line
			content[idx] = line
			break
	content = '\n'.join(content)
	file = open(os.path.join(user_path, f),'wb') 
	file.write(content)  
	file.close()

	

regexes = ['reopen ?\(\"?[\w+-]*\.?\w+\"?,\"r\",stdin\)', 'fopen ?\(\"?[\w+-]*\.?\w+\",[ ]*?\"r\"\)']

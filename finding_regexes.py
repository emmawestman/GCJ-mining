import re

def filter_information(regex,split_at,page):
	list_of_matches = []
	for match in re.findall(regex,page):
		match = match.replace(' ','') #remove blanks
		match = match.replace('\"','') #remove quotes
		if split_at is not None:
        		match = match.split(split_at)[1]
		list_of_matches.append(match)
	return list_of_matches




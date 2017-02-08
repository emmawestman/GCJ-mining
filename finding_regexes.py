import os
import urllib2
import re


def filter_apa(error_message_start,error_message_end,error_string):
    indexes = []
    start_index =error_string.find(error_message_start)
    end_index = error_string.find(error_message_end)
    indexes.append(start_index)
    indexes.append(end_index)
    print "START INDEX " + str(start_index)
    print "END INDEX " + str(end_index)
    return indexes

def filter_information(regex,split_at,page):
    list_of_matches = []
    for match in re.findall(regex,page):
        match = match.replace(' ','') #remove blankspaces
        match = match.replace('\"','') #remove quotes
        list_of_matches.append(match.split(split_at)[1])
    print list_of_matches
    return list_of_matches



#!/usr/bin/python

# Resolve Alias: resolves aliases in a path

from Cocoa import NSString, NSURL

import sys

alias_path = '~/Documents/Chocolate/Shipping Out/08-09-01'

def get_path(alias_path="~/bin/"):
	
	# first resolve tildes
	path = NSString.stringByExpandingTildeInPath(alias_path)
	url = NSURL.URLWithString_(path)
	#data, err = NSURL.bookmarkDataWithContentsOfURL_error_(url, None)
	#url = NSURL.alloc().initByResolvingBookmarkData_options_relativeToUrl_bookmarkDataIsStale_error(path) 
	
	print url
	
	#data =NSURL.URLByResolvingBookmakrData_options_relativeToUrl_bookmarkDataIsStale_Error(
	#			path, None, None, None, None)
	return path
	
	
def test():
	print get_path()
	
if __name__ == '__main__':
	
	test()
    # change to 0 for success, 1 for (partial) failure
	sys.exit(0) 

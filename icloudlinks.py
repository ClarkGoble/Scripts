#!/usr/bin/env python

## icloudlinks.py
##
## Creates a folder of symlinks with the proper names of all the iCloud stores.
## This should be run regularly to ensure that the folder is updated correctly


import sys, os
import re, glob


def getiCloudContents():
    """  
    Gets the folders inside the iCloud directory: ~/Library/Mobile Documents and 
    returns them as an array
    """
    
    return glob.glob(os.path.expanduser('~/Library/Mobile Documents/*'))
    
def makeiCloudDict(contents):
    """
    Given an array of directories this uses a regex to create a dictionary of
    original - converted folder name pairs. The converted folder name is the
    last title in the folder name.
    """
    
    dict = {}
    r = re.compile(".*~(\w+)")
    for c in contents:
        try:
            m = r.match(c)
            name = m.group(1)
            dict[c] = name.capitalize()
            continue
        except:
            continue
            
    return dict 
        
def checkDir():
    """
    Check to see if the ~/iCloud directory exists. If it does delete all the 
    symlinks inside without damaging the files they point at. Otherwise create
    the directory. 
    """
    
    dir = os.path.expanduser('~/iCloud')
    
    if ( os.path.exists( dir ) ):
        for s in glob.glob( dir +"/*" ):
            if ( os.path.islink( s ) ):
                os.remove( s )
    else:
        os.mkdir(  dir )
    
    
    
def makeiCloudFolder():
    """
    Makes a directory in the user's home directory called iCloud that is 
    filled with application names containing their iCloud data. It does
    this by converting the pathname to the hidden iCloud directory in Library
    to the application's title.
    """
    
    appDict = makeiCloudDict(  getiCloudContents() )
    checkDir()
    dir = os.path.expanduser('~/iCloud')
    
    for orig, name in appDict.iteritems():
        print name, orig
        newpath = os.path.join(dir,name) 
        if not os.path.exists( newpath ):
            os.symlink(orig, newpath )
        
    
    
if __name__ == '__main__':
    makeiCloudFolder()
    
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    

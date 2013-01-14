#!/usr/bin/env python

import sys
from Foundation import *
from AppKit import *
import re, os, subprocess
from lxml.html.clean import clean_html, Cleaner
import lxml

## cleanpaste.py
## --------------

## Takes the styled text on the clipboard and removes all formatting such as
## fonts *except* for some specified tags. (Primarily bold and italics)
##
## I typically map this via Quickeys to ctrl-v so that it does a partially
## styled text. Sort of in between regular paste and paste and match style.
## I wish Apple had a way to paste maintaining some style information but
## matching size and font with where you are pasting.
##
## Requires lxml and pyobjc. To install these execute the following at the
## command line:
## sudo easy_install pyobjc
## sudo easy_install lxml
##
## For more information on this script see the posts at Clark's Tech Blog
## http://www.libertypages.com/clarktech/?p=3310


## Cleans up html using lxml to only allow specified tags with their attributes
## removed and remove any style sheet info.

def clean(html):

    if html is None:
        return None
        
    if len(html) < 1:
        return None
    
    # tags to allow    
    tags = ['b', 'i', 'u', 'h1', 'h2','h3','p','strong','em','sub','sup']
    
    # tags to remove AND remove the tag's content
    killtags = ['style']
    
    # keep track of the old attributes considered safe - only relevant if we use
    # lxml in more than this function.  Just good practice to return state.  We
    # have a null set since we want to remove all attributes
    
    old_safe = lxml.html.clean.defs.safe_attrs

    lxml.html.clean.defs.safe_attrs = []
    cleaner = lxml.html.clean.Cleaner(remove_unknown_tags=False, style=False, kill_tags = killtags, 
    safe_attrs_only=True, allow_tags = tags)
    new_html = cleaner.clean_html(html)
    
    lxml.html.clean.defs.safe_attrs = old_safe # not necessary if not used elsewhere
    
    return new_html
    
# function to call textutil on temporary files to convert rtf to html
# path is the path to the temporary file. Returns the data deleting
# the temporary file created in this function but not the one pointed
# to by path
            
def convertrtf(path):  
    q = "textutil -convert html " + path
    subprocess.call(q, shell=True)

    newpath = os.path.splitext(path)[0] + ".html"
    
    data = None
    f = open(newpath, "r")
    try:
        data = f.read()
    finally:
        f.close()
        
    os.remove(newpath)
    return data
    
# given rtf data returns the data converted to html

def convertohtml(data):
    if data is None:
        print "****ERROR"
        return
        
    path = "/tmp/pb.%s.rtf" % os.getpid()
    f = open(path, 'w+t')
    try:
        f.write(data)
    finally:
        f.close()    
    
    newdata = convertrtf(path)
    os.remove(path)
    return newdata

# gets styled text from the clipboard either rtf converted to html, html proper
# or plain text

def getrtfclipboard():
    pb = NSPasteboard.generalPasteboard()
    
    # types of data we can accept: rtf, html, text
    
    type = pb.availableTypeFromArray_([NSPasteboardTypeRTF, NSHTMLPboardType, NSPasteboardTypeString])
    data = None
    if type is None:
        return ""
    if type == NSHTMLPboardType:
        data = pb.stringForType_(type) # get HTML data as text
        return data
    if type == NSPasteboardTypeRTF:
        data = pb.stringForType_(type) # get the data as text
        data = convertohtml(data)
        return data
    data = pb.stringForType_(type) # plain text
    return data
    
# given html this puts it on the clipboard
    
def sethtmlclipboard(html):
    pb = NSPasteboard.generalPasteboard()
    a = NSArray.arrayWithObject_(NSHTMLPboardType)
    pb.declareTypes_owner_(a, None)
    pb.setString_forType_( html, NSHTMLPboardType)
    
    
def test():
    print clean(testtext)
    
def main():
    data = getrtfclipboard()
    newdata =  clean(data)
    print newdata
    sethtmlclipboard(newdata)
        
if __name__ == '__main__':
    main()
    #test()
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    

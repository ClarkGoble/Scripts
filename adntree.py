#!/usr/bin/env python

## adntree.py
#########################################
## With a link to an ADN post on the clipboard this
## opens it up in Safari in TreeView.
## Usually used in concert with Keyboard Maestro to open
## the selected post in TreeView with a single key.

import optparse
import re
import sys
from appscript import *
from osax import OSAX

def opentreeapp(post):
    Safari = app(u'/Applications/Safari.app')
    Safari.activate()
    Safari.make(new=k.document)
    url =  "http://treeview.us/home/thread/"+post+"#"+post
    Safari.documents[0].URL.set(url)
    
def getpostnum(text):
    try:
        lines = text.split("\n")
        l = lines[0].strip()
        match = re.match(r'https://alpha.app.net/.*/post/(\d+)', l)
        post = match.group(1)
    except:
        post = ""
        print "Invalid Format"
        
    return post


def main():
    sa = OSAX()
    url = sa.the_clipboard()
    
    print url
    
    post =  getpostnum(url)
    opentreeapp(post)
        
if __name__ == '__main__':
    main()
    


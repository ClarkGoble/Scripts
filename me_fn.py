#!/usr/bin/python
# -*- coding: utf-8 -*-

## me_fn.py
##
## Reorders footnotes in Mars Edit.

import sys, os
from appscript import *
import re


    
def get_texts():
    """  
    Queries MarsEdit for the body text and extended text and returns them as a dictionary.
    {body:"text",extended:"text"}
    """
    
    doc = app(u'MarsEdit').documents[1]

    blogtext = {}
    blogtext['body'] = doc.body()
    blogtext['extended'] = doc.extended_entry()
    return blogtext
    
def put_texts(blogtext):
    """
    Put into MarsEdit body text and extended text passed to us as a dictionary
    {body:"text",extended:"text"}
    """
    
    doc = app(u'MarsEdit').documents[1]
    doc.body.set(blogtext['body'])
    doc.extended_entry.set(blogtext['extended'])
    


def reorder_footnotes(blogtext):
    """  
    Counts all the footnotes in the document and puts the appropriate number in each.
    """
    
    start_count = 0
    
    # a special token unlikely to appear in our text we use to split on.
    special_token = "##$##"
    
    # replace all occurrences of [#. where # is a number with our special token for later processing
    
    subs = re.sub("\[\d+\. ", special_token, blogtext['body']).split(special_token)
    
    # iterate through pieces adding in our number and footnote text
    
    text = ""
    
    count = 0
    max = len(subs)
    for s in subs:
        count = count + 1
        if count < max:
            text = text + s + "[" + str(count) + ". "    
        else:
            text = text + s
            
    
    blogtext['body'] = text
    text = ""
    
    # now do the same for the extended text
    
    subs = re.sub("\[\d+\. ", special_token, blogtext['extended']).split(special_token)
        
    text = ""

    # update old count to max value of previous run - 1    
    max = len(subs)
    old_count = count - 1
    count = 0
       
    for s in subs:
        count = count + 1
        if count < max:
            text = text + s + "[" + str(count + old_count) + ". "    
        else:
            text = text + s
            
    
    blogtext['extended'] = text
    text = ""
    
    return blogtext
    
    
def main():
    blogtext = get_texts()
    blogtext = reorder_footnotes(blogtext)
    put_texts( blogtext )
    #app(u'BBEdit').activate()
    
if __name__ == '__main__':
    main()
    
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    

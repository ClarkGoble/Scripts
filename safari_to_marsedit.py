#!/usr/bin/python
# -*- coding: utf-8 -*-

### readkit_to_marsedit.py
### Creates a post in MarsEdit for the current tab in Safari

from appscript import *
import sys
import time
from osax import OSAX
from titlecase import titlecase


def get_safari_info():
    """Activates ReadKit and gets the title and url for the selected post"""
    
    # activating Safari's not really needed but makes debugging easier
    app(u'Safari').activate()
    title = app(u'Safari').windows[1].current_tab.name.get() 
    link = app(u'Safari').windows[1].current_tab.URL.get()
        
    return [title, link]


    
def create_marsedit_post(title, link):
    """Creates a MarsEdit post with given html code leaving in rtf mode"""
    
    # create a new Mars Edit document
    ME = app(u'/Applications/MarsEdit.app')
    ME.activate()
    newdoc = ME.make(new=k.document)
    
    # make with category of sideblog  (Where I put short entries)
    
    newdoc.category_names.set(["Sideblog"])

    # set the body text
    
    html = '<a href="{}">{}</a>'.format(link, title)
    newdoc.current_text.set(html)

    # set the post title

    post_title = title.split("\n")[0]    # get rid of multiline titles
    post_title = titlecase(title) # title case the title  
    newdoc.title.set(post_title) # note - must be done last as changing title changes document reference
    

def main():
    title,link = get_safari_info()
    create_marsedit_post(title, link)
    
def test():
    print get_readkit_info()
    
if __name__ == '__main__':
    main()
    #test()
    sys.exit(0)

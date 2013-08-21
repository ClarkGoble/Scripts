#!/usr/bin/python
# -*- coding: utf-8 -*-

### readkit_to_marsedit.py
### Creates a post in MarsEdit for the selected post in ReadKit

from appscript import *
import sys
import time
from osax import OSAX
from titlecase import titlecase


def get_readkit_info():
    """Activates ReadKit and gets the title and url for the selected post"""
    
    app(u'ReadKit').activate()

    # try first method which is for rss display. 
    # If it is in web display mode this will trigger exception
    
    try:
        # UI element for Title is 3 lines: [blog name, title ,  date]
        title_info= app(u'System Events').application_processes[u'ReadKit'].windows[1].splitter_groups[1].scroll_areas[1].UI_elements[1].UI_elements[1].name.get()
        title = title_info.split('\n')[1]
        
        # click the menu for "Copy Link"
        app(u'System Events').application_processes[u'ReadKit'].menu_bars[1].menu_bar_items[7].menus[1].menu_items[1].click()
    
        sa = OSAX()
        link = sa.the_clipboard()
        
        
    except:
        
        # second method assumes it's a web display which is a lost cause getting out of ReadKit
        # send it to Safari instead
        
        app(u'System Events').keystroke("b")
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
    
####################
# Main Functions
####################
    
def main():
    title,link = get_readkit_info()
    create_marsedit_post(title, link)
    
def test():
    print get_readkit_info()
    
if __name__ == '__main__':
    main()
    #test()
    sys.exit(0)

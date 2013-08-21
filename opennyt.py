#!/usr/bin/env python

## opennyt.py
##
## Given a NYT article on the front page this reopens it without the paywall

import sys, os
import time, string, re
from appscript import *

def tab():
    app(u'System Events').keystroke("\t")
    
def downkey():
    app(u'System Events').key_code(125, using=k.command_down)
    
def cr():
    app(u'System Events').keystroke(u'\r')
    app(u'System Events').keystroke(u'\n')
    

def google_search():

    Safari = app(u'Safari')
    title = Safari.windows[1].current_tab.name.get() 
    Safari.activate()
    # Safari.make(at=app.documents.end, new=k.document, with_properties={k.URL: u'http://google.com'})
    Safari.documents[1].URL.set("http://google.com")
    
    time.sleep(1)
    FEdoc = Safari.documents[0].get()
    app(u'System Events').keystroke(title)
    time.sleep(1)
    cr()
    time.sleep(1)
    tab()
#     time.sleep(1)
    downkey()
    downkey()
#     time.sleep(1)
    cr()
    
    
def main():
    google_search()


    
if __name__ == '__main__':
        main()

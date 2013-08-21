#!/usr/bin/env python
# -*- coding: utf-8 -*-

## webtoevernote.py
##--------------------
## Takes the current page in Safari, opens it in reader mode to get rid of the crape
## and then copies it to a new Evernote note.

import time
from appscript import *


def getSafariSummary():
    app(u'Safari').activate()
    app(u'System Events').keystroke(u'r', using=[k.command_down, k.shift_down])
    time.sleep(3)
    app(u'System Events').keystroke(u'a', using=[k.command_down])
    app(u'System Events').keystroke(u'c', using=[k.command_down])
    return 

def getSafariTitle():
    Safari = app(u'/Applications/Safari.app')
    return Safari.windows[1].current_tab.name.get()
    
def makenote(title):
    note = app(u'Evernote').create_note(with_html = "", title=title )
    app(u'Evernote').activate()
    app(u'Evernote').open_note_window(with_ = note)
    time.sleep(1)
    app(u'System Events').keystroke(u'v', using=[k.command_down])
    
    
def main():
    getSafariSummary()
    title = getSafariTitle()
    makenote(title)    

if __name__ == '__main__':
    main()


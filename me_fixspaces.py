#!/usr/bin/python

## fixspaces.py
##
## Removes double spaces

import sys, os
from appscript import *
import time
import string



def replacespaces():
    SE = app(u'System Events')
    SE.keystroke(u'f',using=k.command_down)
    SE.keystroke(u'  ') # two spaces to find
    SE.keystroke(u'\t') # skip to next entry
    SE.keystroke(u' ')  # one space to replace with
    SE.keystroke(u'\t') # skip 3 controls - this might depend upon your
    SE.keystroke(u'\t') # settings in Keyboard pref pane.  You should have 
    SE.keystroke(u'\t') # it set to have tab move between all controls
    SE.keystroke(u' ')  # hit "Replace All"
    SE.keystroke(u'w',using=k.command_down)

def fix():
    app(u'/Applications/MarsEdit.app').activate()
    time.sleep(1)
    
    SE = app(u'System Events')
    
    SE.keystroke(u'b',using=[k.command_down,k.option_down])     # Body Text
    time.sleep(1)
    replacespaces()

    SE.keystroke(u'x',using=[k.command_down,k.option_down])     # Extended Text
    time.sleep(1)
    replacespaces()    
    
if __name__ == '__main__':
    fix()
    
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    

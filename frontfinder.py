#!/usr/bin/env python

###############################
#   frontfinder.py
###############################
#
# Types the path of the front Finder window

import sys
import subprocess
from subprocess import PIPE, Popen

 
def getpath():
    ascript = """'
        tell application "Finder" 
            get quoted form of POSIX path of (target of front Finder window as text)
        end tell
    '"""
    cmd = "osascript -e " + ascript
    
    (out, err) = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True).communicate(None)
    return out
    
    
def typestring(s):
    ascript = """'
        tell application "System Events"
            keystroke "@"
        end tell
    '"""
    
    cmd = "osascript -e " + ascript.replace("@", s)
    
    (out, err) = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True).communicate(None)
    return out
    
def main(argv=None):
    path = getpath().strip()   
    typestring(path)

        
if __name__=='__main__':
    sys.exit(main())
    
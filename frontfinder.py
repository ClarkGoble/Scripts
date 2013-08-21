#!/usr/bin/env python

###############################
#   frontfinder.py
###############################
#
# Types the path of the front Finder window
# Usually used with Keyboard Maestro's text expansions

import sys
import subprocess
from subprocess import PIPE, Popen

# Get the path of the frontmost Finder window
 
def getpath():
    ascript = """'
        tell application "Finder" 
            get quoted form of POSIX path of (target of front Finder window as text)
        end tell
    '"""
    cmd = "osascript -e " + ascript
    
    (out, err) = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True).communicate(None)
    return out
    
    
# Types a string as if it were typed by keyboard. Have to be a bit tricky to avoid
# problems with quotations. (i.e. a path with ' in it.

def typestring(s):
    ascript = """
        tell application "System Events"
            keystroke "@"
        end tell
    EOF
    """
    
    cmd = "osascript << EOF\n " + ascript.replace("@", s)
    
    (out, err) = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True).communicate(None)
    return out
    
def main(argv=None):
    path = getpath().strip()   
    typestring(path)

        
if __name__=='__main__':
    sys.exit(main())
    
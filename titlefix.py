#!/usr/bin/env python

###############################
#   fixchars.py
###############################
#
# Fixes (converts) various character problems.  There are several
# functions that do this
#
# smartdashes - converts normal dashes to long dashes 
# smartquotes - converts normal quotes to smart quotes
#
# If run from the command line it reads standard in
# The flag -html makes it use html code for the characters rather
# than unicode.

from titlecase import titlecase
from appscript import *
import sys, time
from osax import OSAX

def main(argv=None):

    app(u'/Applications/MarsEdit.app').activate()
    time.sleep(1)
    SE = app(u'System Events')
    SE.keystroke(u'c',using=k.command_down)
    sa = OSAX()
    text = sa.the_clipboard().split('\r')
    out = []
    for l in text:
        out.append(titlecase(l))
    
    out_text = '\r'.join(out)
    sa.set_the_clipboard_to( out_text )
    SE.keystroke(u'v',using=k.command_down)
        
if __name__=='__main__':
    sys.exit(main())
    
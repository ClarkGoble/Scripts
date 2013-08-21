#!/usr/bin/env python
# -*- coding: UTF-8 -*-

## me_quote.py
##
## Surrounds the selected text with smart quotes in MarsEdit

import sys, os
from appscript import *
import time
import string

def smartreplace():
    """  
    gets the selection, modifies it with quotes, and the puts that back over the selection
    """
    
    st = app(u'MarsEdit').documents[1].selected_text()

    st = u"“" + st + u"”"
    app(u'MarsEdit').documents[1].selected_text.set(st)
    return
    
def main():
    smartreplace()

if __name__=='__main__':
    sys.exit(main())
    
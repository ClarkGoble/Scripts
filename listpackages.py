#!/usr/bin/env python

from pkg_resources import Environment
import sys

def listall():
    c = 0
    for p in Environment():
        c = c + 1
        print "%5d  "%c + p
        
    
listall()
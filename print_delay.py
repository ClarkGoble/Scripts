#!/usr/bin/env python

## Prints multiple copies of a page with a delay between each. 
## Primarily for use with stickers that gum up the printer if it doesn't 
## cool down between printing

import string, sys, time, shutil
from appscript import *
        
def printpages( numberofpages):
    
    doc = app(u'Pages').documents[1]
    
    for i in range(0,numberofpages):
        print i
        doc.print_()
        time.sleep(10)
            
if __name__ == '__main__':
    printpages(35)
        
        
            
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    
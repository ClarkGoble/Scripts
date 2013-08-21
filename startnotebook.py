#!/usr/bin/env python

import sys
from appscript import *
import time
from plumbum import BG, local
from plumbum.cmd import grep, ps, wc

def check_notebook():
    chain = ps["aux"] | grep["ipython notebook"]
    result = chain()
    
    if "/usr/local/bin/ipython notebook" in result:
        print "Notebook Running"
        return True
    
    return False
    
def start_notebook():
    #command = "/usr/local/bin/ipython notebook --pylab inline --no-browser --NotebookManager.notebook_dir='/Users/clarkgoble/projects'&"
    
    ipython = local["/usr/local/bin/ipython"]
    ipython["notebook", "--pylab", "--no-browser", "--NotebookManager.notebook_dir='/Users/clarkgoble/projects'"] & BG
    
    # takes a little bit of time to startup - want to pause before attaching
    time.sleep(2)
                 
def attach_notebook():
    C = app(u'/Applications/Google Chrome.app')
    C.make(new=k.window)
    
    C.windows[1].active_tab.URL.set("http://127.0.0.1:8888")
    C.activate()    

    
def main():
    if not check_notebook():
        start_notebook()
        
    attach_notebook()
            
if __name__=='__main__':
    sys.exit(main())
    
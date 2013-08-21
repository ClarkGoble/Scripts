#!/usr/bin/env python

###############################
#   today.py
###############################
#
# Types today's date formated

import sys, datetime, string
from appscript import *
 
def getdate():
    d=datetime.date.today()
    d = d + datetime.timedelta(-1)
    return d.strftime("%m/%d/%Y")
    
def typestring(s):
    SE = app(u'System Events')
    
    for i in range(0,len(s)):
        c = s[i]
        
        if c == '\n':
            continue
            
        if c in string.ascii_uppercase:
            SE.keystroke(s[i], using=k.shift_down)
        else:
            SE.keystroke(s[i])
                   
def main(argv=None):
    print getdate()    

        
if __name__=='__main__':
    sys.exit(main())
    
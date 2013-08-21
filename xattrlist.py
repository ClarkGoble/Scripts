#!/usr/bin/env python

import sys, os, os.path
from plumbum import BG, local
from plumbum.cmd import xattr, xxd, plutil
import optparse

def list_attr(path):
    attr_list = xattr[path]().split("\n")
    
    for a in attr_list:
        print a
        if a == u"":
            continue
        if a=="com.apple.FinderInfo":
            continue
        
        
        chain = xattr["-p",a,path]  | xxd["-p","-r"] | plutil["-convert","xml1","-o","-", "-"]
        text = chain() .split("\n")
        for t in text:
            print "  ", t
    return
    
def main(args):
    for a in args:
        if not os.path.exists(a):
            continue
            
        print "File: ", a
        list_attr(a)
            
if __name__=='__main__':
    option_parser = optparse.OptionParser(usage='%prog files')
    options, args = option_parser.parse_args()
    
    if len(args) != 1:
        option_parser.print_help()
        sys.exit(1)
        
    sys.exit(main(args))
    
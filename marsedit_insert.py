#!/usr/bin/python
# -*- coding: utf-8 -*-

## marsedit_insert.py
## --------------

## Inserts HTML text into MarsEdit at the current insertion point

import string, sys, time, shutil
from appscript import *
from osax import OSAX
import datetime, re
import optparse

## For logging. Since I typically run this via command scripts activated by 
## keystrokes you can't use print statements for debugging. A nice technique
## is to use the logging feature of Python and set it so it is a rotating 
# log. I use the location in my script but you can use whatever you want.

import logging
import logging.handlers

LOG_FILE = '/Users/clarkgoble/bin/text/marsedit_insert.log'
my_log = logging.getLogger('theLog')
my_log.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=10)
my_log.addHandler(handler)
    
# Inserts text by saving clipboard content and then using clipboard to 
# insert the text. We paste by accessing MarsEdit's menubar.

def insert_text_cb(text):
    
    sa = OSAX()

    # save old clipboard (only text part)
    oldtext = sa.the_clipboard()
    
    # put our text on clipboard
    sa.set_the_clipboard_to(text)
 
    # paste clipboard
    ME = app(u'System Events').application_processes[u'MarsEdit']
    ME.menu_bars[1].menu_bar_items[4].menus[1].menu_items[6].click()

    # restore old clipboard 
    # need to pause so we don't replace clipboard before it is pasted
    time.sleep(.5)

    sa.set_the_clipboard_to( oldtext )
    

# type back arrow presses number of times

def backarrow(presses=1):
    for i in range(presses):
        app(u'System Events').key_code(123)
        
# type forward arrow presses number of times

def forwardarrow(presses=1):
    for i in range(presses):
        app(u'System Events').key_code(124)
        
# type command - down arrow

def cmddownkey():
    app(u'System Events').key_code(125, using=k.command_down)
        
# type text s as if it were typed on the keyboard

def typestring(s):
    
    for i in range(0,len(s)):
        c = s[i]
        
        if c == '\n':
            continue
            
        if c in string.ascii_uppercase:
            app(u'System Events').keystroke(s[i], using=k.shift_down)
        else:
            app(u'System Events').keystroke(s[i])

# returns the text of the format menu in the Post menu in MarsEdit
# should be Edit Rich Text or Edit HTML Text depending upon mode

def geteditmode():
    app(u'/Applications/MarsEdit.app').activate()
    SE = app(u'System Events').application_processes[u'MarsEdit']
    menu = SE.menu_bars[1].menu_bar_items[7].menus[1].menu_items[3]
    menu_name = menu.name.get()
    return menu_name
    
# put ourselves in HTML editing more in MarsEdit

def sethtmlmode():
    
    app(u'/Applications/MarsEdit.app').activate()
    SE = app(u'System Events').application_processes[u'MarsEdit']
    menu = SE.menu_bars[1].menu_bar_items[7].menus[1].menu_items[3]
    menu_name = menu.name.get()
    
    if  "Edit HTML" in menu_name:
    
        # click HTML mode
        
        SE.menu_bars[1].menu_bar_items[7].menus[1].menu_items[3].click()
        
        # skip over </p> tag MarsEdit automatically puts at end since when
        # we switch to html mode MarsEdit puts us at the end of the text
        # rather than maintaining our edit position
        
        backarrow(4)    
        
# put ourselves in rtf editing more in MarsEdit

def setrtfmode():

    app(u'/Applications/MarsEdit.app').activate()
    SE = app(u'System Events').application_processes[u'MarsEdit']
    menu = SE.menu_bars[1].menu_bar_items[7].menus[1].menu_items[3]
    menu_name = menu.name.get()
    
    if  "Edit Rich" in menu_name:
    
        # click rtf mode
        
        SE.menu_bars[1].menu_bar_items[7].menus[1].menu_items[3].click()
        
    # go to end
    cmddownkey()


# inserts tag to make HTML so that the character prior to the cursor in
# MarsEdit looks like a keyboard key

def inserttags():

    # move back before typed character
    backarrow()
    typestring('<span class="keyboardshortcut">')
    forwadarrow()
    typestring('</span>')

# inserts character c into text as if it were a keyboard key

def makekey(c = u"X"):
    my_log.info("inside makekey")
    insert_text_cb('<span class="keyboardshortcut">' + c + '</span>')
    
# functions for specially named keys

def shiftkey():
    makekey( u"\u2318" )
    
def cmdkey():
    makekey( u"\u2318" )
    
def caplockkey():
    makekey( u"\u21EA" )
    
def ctrlkey():
    makekey( u"\u2303")
    
def deletekey():
    makekey( u"\u232B")
    
def optionkey():
    makekey( u"\u2325")

def shiftkey():
    makekey( u"\u21E7")
    
def tabkey():
    makekey( u"\u21E5")
    
# tries to evaluate the keyname in case it is a function otherwise just
# generates html for the text as a key

def htmlkey( keyname ):
    try:
        my_log.info("Try:"+ keyname )
        eval( keyname + "()" )
        my_log.info("Success:"+keyname )
    except:
        my_log.info("Except: " + keyname)
        makekey( keyname )


def test():
    htmlkey( "tabkey" )
    htmlkey( "test" )
    
    
if __name__ == '__main__':
    option_parser = optparse.OptionParser(usage='%prog keyname1 keyname2')
    options, args = option_parser.parse_args()
    if len(args) < 1:
        test()
        
    # we need to be in MarsEdit's HTML mode
    
    sethtmlmode()
    
    for a in range(len(args)):
        htmlkey( args[a] )

    
    # put us back in rtf mode
    setrtfmode()
            
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    
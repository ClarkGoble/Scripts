#!/usr/bin/python

import os
from appscript import *
import time, string

def typestring(s):
    
    for i in range(0,len(s)):
        c = s[i]
        
        if c == '\n':
            continue
            
        if c in string.ascii_uppercase:
            app(u'System Events').keystroke(s[i], using=k.shift_down)
        else:
            app(u'System Events').keystroke(s[i])
        #print s[i]
                
def backtab():
    app(u'System Events').keystroke("\t", using=k.shift_down)
    
def tab():
    app(u'System Events').keystroke("\t")
    
def cr():
    app(u'System Events').keystroke(u'\r')
    app(u'System Events').keystroke(u'\n')

# sends cmd-opt-f which in mail selects the search widget
def select_search():
    app(u'Mail').activate()
    app(u'System Events').keystroke(u'f', using=[k.command_down, k.option_down])

def makesmartmailbox(email=u'clark@amanochocolate.com'):
    M = app(u'Mail')
    SE = app(u'System Events').processes[u'Mail']
    
    # Open New Smart Mailbox Sheet
    M.activate()
    SE.menu_bars[1].menu_bar_items[u'Mailbox'].menus[1].menu_items[u'New Smart Mailbox\u2026'].click()        

    SMB = app(u'System Events').processes[u'Mail'].windows[1].sheets[1]

    # Set Smart Mailbox Name
    SMB.text_fields[1].value.set(email)
    
    # Set rules as any 
    SMB.pop_up_buttons[1].click()
    SMB.pop_up_buttons[1].menus[1].menu_items[1].click()
    # switch to menu_items[2] to click "all"
    
    # Select First Rule
    SMB.scroll_areas[1].pop_up_buttons[1].click()
    
    # Click "From" (2cd menu item)
    SMB.scroll_areas[1].pop_up_buttons[1].menus[1].menu_items[2].click()
    SMB.scroll_areas[1].text_fields[1].value.set(email)
    
    # Create Second Rule
    SMB.scroll_areas[1].buttons[u'add criterion'].click()
    # the new rule type is button 3
    SMB.scroll_areas[1].pop_up_buttons[3].click()   
    SMB.scroll_areas[1].pop_up_buttons[3].menus[1].menu_items[2].click()
    # the new text area is text field 2
    SMB.scroll_areas[1].text_fields[2].value.set(email)
    
    # include messages from sent
    SMB.checkboxes[u'Include messages from Sent'].click()
    
    # Save the rule
    SMB.buttons[u'OK'].click()
    
def test():
    makesmartmailbox(u'clark@amanochocolate.com')
    
if __name__ == '__main__':
    test()

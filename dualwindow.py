#!/usr/bin/python

## Creates two Finder windows, each covering half the screen from the frontmost 
## finder window.

import objc
from AppKit import *
from appscript import *
from osax import OSAX
import sys
from subprocess import Popen, PIPE

def getscreensize():
	# Using PyObjC gets the size of the main screen minus the dock & menu
	# returns it as a list
		
	rect = NSScreen.mainScreen().visibleFrame()
	return  [int(rect.origin.x), int(rect.origin.y), int(rect.size.width), int(rect.size.height)]
	
def make_finder_dual(screen):
	# Given a screen size creates two adjacent Finder windows taking up all the specified
	# screen size.  One of the windows is the front most window while the second window
	# is a new window but with the same location as the front window.
	
	Finder = app(u'/System/Library/CoreServices/Finder.app')
	
	# Make sure we have a finder window - otherwise make one
	
	if len( Finder.windows() ) < 1 :
		return
	
	# Front Window info 
	
	old_view = Finder.windows[1].current_view()
	old_target = Finder.windows[1].target()
	toolbarvis = Finder.windows[1].toolbar_visible()
	
	# Set Front Window  
	print screen
	
	Finder.windows[1].bounds.set([screen[0] + 1, screen[1], screen[2], screen[3]/2])
	#Finder.windows[1].bounds.set([ 1,40, 1920, 500])
	# Set New Window
	
	new_window = Finder.make(new=k.Finder_window)
	new_window.bounds.set( [screen[0] + 1, screen[3]/2, screen[2], screen[3] ] )
	#new_window.bounds.set( [1, 801, 1920, 900 ] )
	new_window.current_view.set( old_view )
	new_window.target.set( old_target )
	new_window.toolbar_visible.set( toolbarvis )


	
if __name__ == '__main__':

    screen = getscreensize()
    make_finder_dual(screen)
    
    
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0)
	
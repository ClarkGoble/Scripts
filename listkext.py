#!/usr/bin/python
 
import sys
from subprocess import Popen, PIPE
import re
 
 
def nonapplekext():
 
	# Run the kextstat command which lists *all* kernel extensions
	p = Popen(["kextstat"],stdout=PIPE)
 
	kext = []		# our list of extensions
 
	while 1:
		o = p.stdout.readline()
 
		# keep reading lines from the kextstat command until there are no more
		if o == '' and p.poll() != None:
			break
 
		# the company name starts at character 44
		l = o[52:]
 
		#  get rid of the extra info at the end
		t = re.sub("<.*>","", l)
 
		# exclude all the Apple supplied extensions
		if l[0:9] != "com.apple":
			kext.append(t[:-2])
 
	# return the sorted list sans the header
	return sorted(kext[1:])
 
 
if __name__ == '__main__':
	kext = nonapplekext()
	print '\n'.join(kext)
 
    	# change to 0 for success, 1 for (partial) failure
	sys.exit(0)
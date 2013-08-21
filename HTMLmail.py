#!/usr/bin/python

import os
from appscript import *
import time, string


myHTML = """
<html>
<body>
<p>
This is a test message. <b>It works!</b>
</p>
<p>
This is another paragraph.
</p>
</body>
</html>
"""
    
def mailfromSafari(filename):
    
    # open filename in Safari
    
    S = app('Safari')
    S.make(at=app.documents.before, new=k.document)
    fn = u'file://'+filename
    S.documents[1].source.set(myHTML)
    return
    
    S.documents[1].URL.set(fn)
    S.activate()
    
    # create mail message with HTML from Safari
    
    SE = app(u'System Events')
    SE.keystroke(u'i', using=k.command_down)
    time.sleep(2)
    S.documents[1].close()
    time.sleep(1)

def fillmail(tomail = "who@somwhere.com", subject = "subject"):
    app('Mail').activate()
    SE = app(u'System Events')
    SE.processes[u'Mail'].windows[1].scroll_areas[2].text_fields[1].value.set(tomail)
    SE.processes[u'Mail'].windows[1].text_fields[1].value.set(subject)
    
    
def createHTMLMail(htmltext = myHTML):
    filename = '/tmp/mailhtml.%s.html' % os.getpid()
    tempfile = open(filename, "w")
    
    try:
        tempfile.write(htmltext)
    finally:
        tempfile.close()
        
    mailfromSafari(filename)
    
    os.remove(filename)
    
    fillmail("clark@amanochocolate.com","subject")
    
def main():
    createHTMLMail()
    
if __name__ == '__main__':
    main()

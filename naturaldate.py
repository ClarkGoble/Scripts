#!/usr/bin/env python 
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import datetime
from osax import OSAX
from appscript import *

def gettime():
    # by specifying System Events you keep python from
    # creating a GUI app
    
    sa = OSAX("StandardAdditions", name="System Events")
    
    # bring dialog to front
    sa.activate()
    data = sa.display_dialog("Test",buttons=["OK","Cancel"],
                    default_button=1, 
                    default_answer="Event - tomorrow")
    
    if data == None:
        return ""
    
    if data[k.button_returned] == "OK":
        return data[k.text_returned]
    else:
        return ""
      
def datetimeFromString( s ):
    # parse date and time from natural string.
    # http://stackoverflow.com/questions/1810432/handling-the-different-results-from-parsedatetime

    c = pdc.Constants()
    p = pdt.Calendar(c)
    result, what = p.parse( s )
    dt = 0

    if what in (1,2,3):
        # result is struct_time
        dt = datetime.datetime( *result[:6] )
        
    if what == 0:
        # Failed to parse
        return ""
    return dt

def setcal(title, rd):
    app(u'iCal').activate()
    event = app(u'iCal').calendars[u'Work'].events.end.make(new=k.event)
    event.summary.set( title )
    event.description.set( title )
    event.start_date.set( rd )  
    
def main():
    nattime  =  gettime()

    if nattime == "":
        return
    
    title = nattime.split("-")[0]
    
    NLPDate = datetimeFromString(nattime)
    realdate =  NLPDate
    setcal( title, realdate )

if __name__ == '__main__':    
    main()
    

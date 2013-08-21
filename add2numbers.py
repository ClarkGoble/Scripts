#!/usr/bin/env python

## add2numbers.py
## --------------
##
## Puts the selected addresses from Address Book into Numbers. I've included the
## code for it to work in Excel as well. Just comment out the appropriate line.


from appscript import *
import sys


# Create a new numbers spreadsheet by clicking on the "New" menu. (Numbers 09 doesn't
# allow scripting of new document creation.

def preparenumbers():
    app(u'Numbers').activate()
    app(u'System Events').application_processes[u'Numbers'].menu_bars[1].menu_bar_items[3].menus[1].menu_items[1].click()

# Given a row number and dictionary this fills in the appropriate Numbers row

def fillnumbers( rownumber, ad ):
    
    table = app(u'Numbers').documents[1].sheets[1].tables[1]
    
    table.columns[1].cells[rownumber].value.set( rownumber )
    table.columns[2].cells[rownumber].value.set( ad["company"] )
    table.columns[3].cells[rownumber].value.set( ad["name"] )
    table.columns[4].cells[rownumber].value.set( ad["street"] )
    table.columns[5].cells[rownumber].value.set( ad["city"] )
    table.columns[6].cells[rownumber].value.set( ad["state"] )
    table.columns[7].cells[rownumber].value.set( ad["zip"] )
    table.columns[8].cells[rownumber].value.set( ad["phone"])
    
# Given a row number and dictionary this fills in the appropriate Excel row

def fillexcel( rownumber, ad ):
    MS = app('/Applications/Microsoft Office 2011/Microsoft Excel')
    
    MS.cells[ "A" + str(rownumber) ].value.set( ad["company"] )
    MS.cells[ "B" + str(rownumber) ].value.set( ad["first"] )
    MS.cells[ "C" + str(rownumber) ].value.set( ad["last"] )
    MS.cells[ "D" + str(rownumber) ].value.set( ad["street"] )
    MS.cells[ "E" + str(rownumber) ].value.set( ad["city"] )
    MS.cells[ "F" + str(rownumber) ].value.set( ad["state"] )
    MS.cells[ "G" + str(rownumber) ].value.set( ad["zip"] )
    MS.cells[ "H" + str(rownumber) ].value.set( ad["phone"])

# given an address from Address book this cleans it up and returns a
# dictionary with the appropriate data
    
def clean_address( a ):
        ad = {}
        row = row + 1
        
        if a == None:
            continue
    
        if a.company.get() == False:
            ad["company"] = ""
        else:
            ad["company"] = a.name()
        
        # print row, ad["company"], first + " " + last
        
        
        if a.first_name() is not None:
            if a.last_name() == k.missing_value:
                first = u" "
            else:
                first = a.first_name() 
        else:
            print "none"
            first= u" "

        if a.last_name() is not None:
            if a.last_name() == k.missing_value:
                last =  u" "
            else:
                last =  a.last_name() 
        else:
            last = u" " 
            
        ad["name"] = first + u" " + last
        ad['first'] = first
        ad['last'] = last
        
        if len(a.phones()) >0:
            ad["phone"] = a.phones()[0].value()
        else:
            ad["phone"] = "801-655-1996"

        if len( a.addresses() ) > 0:
            if len((a.addresses())[0].street()) > 0:
                ad["street"] = (a.addresses())[0].street()
                ad["city"] = (a.addresses())[0].city()
                ad["state"] = (a.addresses())[0].state()
                ad["zip"] = (a.addresses())[0].zip()
            else:
                ad["street"] = ""
                ad["city"] = ""
                ad["state"] = ""
                ad["zip"] = ""       
        else:
            ad["street"] = ""
            ad["city"] = ""
            ad["state"] = ""
            ad["zip"] = ""         

    return ad
    
def get_address():
    AB = app(u'/Applications/Address Book.app')
    
    # if you prefer to get all of a group uncomment out this
    # line and comment up the subsequent line. And add the appropriate
    # group name
    
    # addresses = AB.groups[u'Clients'].people.get()
    addresses = AB.selection.get()
    
    row = 1
    
    # create header in Numbers
    ad = {"company":"Company", "name":"Name", "first":"First","last":"Last", "phone":"Phone", "street":"Street", 
            "city":"City", "state":"State", "zip":"Zip","phone":"Phone" }
    
    #fillnumbers( 1, ad )
    fillexcel(1, ad)
    
    for a in addresses:
        ad = clean_address(a)
        #fillnumbers( row, ad )
        fillexcel( row, ad )
        
def test():
    preparenumbers()
    
if __name__ == '__main__':
    test()
    #get_address()
    
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    